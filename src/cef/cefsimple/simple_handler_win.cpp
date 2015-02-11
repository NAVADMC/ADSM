// Copyright (c) 2013 The Chromium Embedded Framework Authors. All rights
// reserved. Use of this source code is governed by a BSD-style license that
// can be found in the LICENSE file.

#include "cefsimple/simple_handler.h"

#include <string>
#include <windows.h>
#include <ShlObj.h>
#include <objbase.h>
#include <shellapi.h>

#include "include/cef_browser.h"
#include "include/wrapper/cef_helpers.h"
#include "include/resource.h"

void SimpleHandler::OnTitleChange(CefRefPtr<CefBrowser> browser,
	const CefString& title) {
	CEF_REQUIRE_UI_THREAD();

	CefWindowHandle hwnd = browser->GetHost()->GetWindowHandle();
	SetWindowText(hwnd, std::wstring(title).c_str());
}

void SimpleHandler::SendNotification(NotificationType type, CefRefPtr<CefBrowser> browser, int percentComplete, CefRefPtr<CefDownloadItemCallback> callback) {
	std::wstring caption;
	std::wstringstream message, path;
	HRESULT hr;
	switch (type) {
	case NOTIFY_DOWNLOAD_STARTED:
		hr = CoCreateInstance(CLSID_ProgressDialog, NULL, CLSCTX_ALL, IID_IProgressDialog, reinterpret_cast<void**>(&progress_dialog_ptr_));
		if (SUCCEEDED(hr))
		{
			caption = L"Saving file";
			progress_dialog_ptr_->SetLine(DWORD(1), PCWSTR(caption.c_str()), FALSE, NULL);
			message << std::wstring(CefString(this->GetLastDownloadFile()));
			progress_dialog_ptr_->SetLine(DWORD(2), PCWSTR(message.str().c_str()), FALSE, NULL);

			progress_dialog_ptr_->StartProgressDialog(browser->GetHost()->GetWindowHandle(), NULL, PROGDLG_NORMAL, NULL);
		}
		break;
	case NOFITY_DOWNLOAD_IN_PROGRESS:
		if (progress_dialog_ptr_->HasUserCancelled()) {
			callback->Cancel();
			break;
		}
		message << percentComplete << L"% Complete";
		progress_dialog_ptr_->SetTitle(PCWSTR(message.str().c_str()));
		progress_dialog_ptr_->SetProgress(DWORD(percentComplete), (DWORD)100);
		break;
	case NOTIFY_DOWNLOAD_CANCELED:
	case NOTIFY_DOWNLOAD_COMPLETE:
		if (SUCCEEDED(progress_dialog_ptr_->StopProgressDialog())) {
			progress_dialog_ptr_->Release();
		}
		caption = L"Save Status";
		if (type == NOTIFY_DOWNLOAD_COMPLETE) {
			message << L"File \"" <<
				std::wstring(CefString(this->GetLastDownloadFile())) <<
				L"\" was saved successfully.";
		}
		else {
			message << L"File save was cancelled.";
		}
		MessageBox(browser->GetHost()->GetWindowHandle(),
			message.str().c_str(),
			caption.c_str(),
			MB_OK | MB_ICONINFORMATION);
		break;
	default:
		return;
	}
}

std::string SimpleHandler::GetDownloadPath(const std::string& file_name) {
	TCHAR szFolderPath[MAX_PATH];
	std::string path;

	// Save the file in the user's "My Documents" folder.
	if (SUCCEEDED(SHGetFolderPath(NULL, CSIDL_PERSONAL | CSIDL_FLAG_CREATE,
		NULL, 0, szFolderPath))) {
		path = CefString(szFolderPath);
		path += "\\" + file_name;
		name_selected_ = TRUE;
	}

	return path;
}

void SimpleHandler::HandleExternalURL(CefString url) {
	ShellExecuteW(NULL, TEXT("open"), url.c_str(), NULL, NULL, SW_NORMAL);
	return;
}
