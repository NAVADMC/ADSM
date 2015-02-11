// Copyright (c) 2013 The Chromium Embedded Framework Authors. All rights
// reserved. Use of this source code is governed by a BSD-style license that
// can be found in the LICENSE file.

#include "cefsimple/simple_handler.h"

#include <sstream>
#include <string>

#include "include/base/cef_bind.h"
#include "include/cef_app.h"
#include "include/wrapper/cef_closure_task.h"
#include "include/wrapper/cef_helpers.h"

namespace {

	SimpleHandler* g_instance = NULL;

}  // namespace

SimpleHandler::SimpleHandler()
	: is_closing_(false) {
	DCHECK(!g_instance);
	g_instance = this;
	progress_started_ = FALSE; name_selected_ = FALSE;
}

SimpleHandler::~SimpleHandler() {
	g_instance = NULL;
}

// static
SimpleHandler* SimpleHandler::GetInstance() {
	return g_instance;
}

void SimpleHandler::OnAfterCreated(CefRefPtr<CefBrowser> browser) {
	CEF_REQUIRE_UI_THREAD();

	// Add to the list of existing browsers.
	browser_list_.push_back(browser);
}

bool SimpleHandler::DoClose(CefRefPtr<CefBrowser> browser) {
	CEF_REQUIRE_UI_THREAD();

	// Closing the main window requires special handling. See the DoClose()
	// documentation in the CEF header for a detailed destription of this
	// process.
	if (browser_list_.size() == 1) {
		// Set a flag to indicate that the window close should be allowed.
		is_closing_ = true;
	}

	// Allow the close. For windowed browsers this will result in the OS close
	// event being sent.
	return false;
}

void SimpleHandler::OnBeforeClose(CefRefPtr<CefBrowser> browser) {
	CEF_REQUIRE_UI_THREAD();

	// Remove from the list of existing browsers.
	BrowserList::iterator bit = browser_list_.begin();
	for (; bit != browser_list_.end(); ++bit) {
		if ((*bit)->IsSame(browser)) {
			browser_list_.erase(bit);
			break;
		}
	}

	if (browser_list_.empty()) {
		// All browser windows have closed. Quit the application message loop.
		CefQuitMessageLoop();
	}
}

void SimpleHandler::OnLoadError(CefRefPtr<CefBrowser> browser,
	CefRefPtr<CefFrame> frame,
	ErrorCode errorCode,
	const CefString& errorText,
	const CefString& failedUrl) {
	CEF_REQUIRE_UI_THREAD();

	// Don't display an error for downloaded files.
	if (errorCode == ERR_ABORTED)
		return;

	// Display a load error message.
	std::stringstream ss;
	ss << "<html><body bgcolor=\"white\">"
		"<h2>Failed to load URL " << std::string(failedUrl) <<
		" with error " << std::string(errorText) << " (" << errorCode <<
		").</h2></body></html>";
	frame->LoadString(ss.str(), failedUrl);
}

void SimpleHandler::CloseAllBrowsers(bool force_close) {
	if (!CefCurrentlyOn(TID_UI)) {
		// Execute on the UI thread.
		CefPostTask(TID_UI,
			base::Bind(&SimpleHandler::CloseAllBrowsers, this, force_close));
		return;
	}

	if (browser_list_.empty())
		return;

	BrowserList::const_iterator it = browser_list_.begin();
	for (; it != browser_list_.end(); ++it)
		(*it)->GetHost()->CloseBrowser(force_close);
}

void SimpleHandler::OnBeforeDownload(
	CefRefPtr<CefBrowser> browser,
	CefRefPtr<CefDownloadItem> download_item,
	const CefString& suggested_name,
	CefRefPtr<CefBeforeDownloadCallback> callback) {
	CEF_REQUIRE_UI_THREAD();

	// Continue the download and show the "Save As" dialog.
	if (!name_selected_ && !progress_started_) {
		callback->Continue(GetDownloadPath(suggested_name), true);
	}
}

void SimpleHandler::OnDownloadUpdated(
	CefRefPtr<CefBrowser> browser,
	CefRefPtr<CefDownloadItem> download_item,
	CefRefPtr<CefDownloadItemCallback> callback) {
	CEF_REQUIRE_UI_THREAD();

	if (name_selected_ && download_item->GetFullPath() != "") {
		SetLastDownloadFile(download_item->GetFullPath());
		SendNotification(NOTIFY_DOWNLOAD_STARTED, browser);
		name_selected_ = FALSE;
		progress_started_ = TRUE;
	}

	if (download_item->IsInProgress() && progress_started_) {
		if (download_item->GetFullPath() == last_download_file_) {
			SendNotification(NOFITY_DOWNLOAD_IN_PROGRESS, browser, download_item->GetPercentComplete(), callback);
		}
	}

	if (download_item->IsCanceled()) {
		SendNotification(NOTIFY_DOWNLOAD_CANCELED, browser);
		progress_started_ = FALSE;
	}

	if (download_item->IsComplete()) {
		SendNotification(NOTIFY_DOWNLOAD_COMPLETE, browser);
		progress_started_ = FALSE;
	}
}

bool SimpleHandler::OnBeforeBrowse(
	CefRefPtr<CefBrowser> browser,
	CefRefPtr<CefFrame> frame,
	CefRefPtr<CefRequest> request,
	bool is_redirect) {
	CEF_REQUIRE_UI_THREAD();

	std::string app_url = "http://127.0.0.1:8000";
	CefString url = request->GetURL();

	if (url.ToString().compare(0, 21, app_url) == 0) {
		return false;
	}
	else {
		HandleExternalURL(url);
		return true;
	}
}

void SimpleHandler::SetLastDownloadFile(const std::string& fileName) {
	CEF_REQUIRE_UI_THREAD();
	last_download_file_ = fileName;
}

std::string SimpleHandler::GetLastDownloadFile() const {
	CEF_REQUIRE_UI_THREAD();
	return last_download_file_;
}

void SimpleHandler::OnBeforeContextMenu(CefRefPtr<CefBrowser> browser,
	CefRefPtr<CefFrame> frame,
	CefRefPtr<CefContextMenuParams> params,
	CefRefPtr<CefMenuModel> model) {
	CEF_REQUIRE_UI_THREAD();

	model->Clear();
}
