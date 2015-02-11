// Copyright (c) 2013 The Chromium Embedded Framework Authors. All rights
// reserved. Use of this source code is governed by a BSD-style license that
// can be found in the LICENSE file.

#ifndef CEF_TESTS_CEFSIMPLE_SIMPLE_HANDLER_H_
#define CEF_TESTS_CEFSIMPLE_SIMPLE_HANDLER_H_

#include "include/cef_client.h"
#include <ShlObj.h>

#include <list>

class SimpleHandler : public CefClient,
	public CefDisplayHandler,
	public CefDownloadHandler,
	public CefContextMenuHandler,
	public CefLifeSpanHandler,
	public CefLoadHandler,
	public CefRequestHandler {
public:
	SimpleHandler();
	~SimpleHandler();

	// Provide access to the single global instance of this object.
	static SimpleHandler* GetInstance();

	// CefClient methods:
	virtual CefRefPtr<CefDisplayHandler> GetDisplayHandler() OVERRIDE{
		return this;
	}
		virtual CefRefPtr<CefLifeSpanHandler> GetLifeSpanHandler() OVERRIDE{
		return this;
	}
		virtual CefRefPtr<CefLoadHandler> GetLoadHandler() OVERRIDE{
		return this;
	}
		virtual CefRefPtr<CefDownloadHandler> GetDownloadHandler() OVERRIDE{
		return this;
	}
		virtual CefRefPtr<CefContextMenuHandler> GetContextMenuHandler() OVERRIDE{
		return this;
	}
		virtual CefRefPtr<CefRequestHandler> GetRequestHandler() OVERRIDE{
		return this;
	}

		// CefDisplayHandler methods:
		virtual void OnTitleChange(CefRefPtr<CefBrowser> browser,
		const CefString& title) OVERRIDE;

	// CefLifeSpanHandler methods:
	virtual void OnAfterCreated(CefRefPtr<CefBrowser> browser) OVERRIDE;
	virtual bool DoClose(CefRefPtr<CefBrowser> browser) OVERRIDE;
	virtual void OnBeforeClose(CefRefPtr<CefBrowser> browser) OVERRIDE;

	// CefLoadHandler methods:
	virtual void OnLoadError(CefRefPtr<CefBrowser> browser,
		CefRefPtr<CefFrame> frame,
		ErrorCode errorCode,
		const CefString& errorText,
		const CefString& failedUrl) OVERRIDE;

	// CefDownloadHandler methods
	virtual void OnBeforeDownload(
		CefRefPtr<CefBrowser> browser,
		CefRefPtr<CefDownloadItem> download_item,
		const CefString& suggested_name,
		CefRefPtr<CefBeforeDownloadCallback> callback) OVERRIDE;
	virtual void OnDownloadUpdated(
		CefRefPtr<CefBrowser> browser,
		CefRefPtr<CefDownloadItem> download_item,
		CefRefPtr<CefDownloadItemCallback> callback) OVERRIDE;

	// CefRequestHandler methods
	virtual bool OnBeforeBrowse(
		CefRefPtr<CefBrowser> browser,
		CefRefPtr<CefFrame> frame,
		CefRefPtr<CefRequest> request,
		bool is_redirect) OVERRIDE;

	void HandleExternalURL(CefString url);

	void SetLastDownloadFile(const std::string& fileName);
	std::string GetLastDownloadFile() const;

	// CefContextMenuHandler methods
	virtual void OnBeforeContextMenu(CefRefPtr<CefBrowser> browser,
		CefRefPtr<CefFrame> frame,
		CefRefPtr<CefContextMenuParams> params,
		CefRefPtr<CefMenuModel> model) OVERRIDE;

	// Send a notification to the application. Notifications should not block the
	// caller.
	enum NotificationType {
		NOTIFY_CONSOLE_MESSAGE,
		NOTIFY_DOWNLOAD_COMPLETE,
		NOTIFY_DOWNLOAD_ERROR,
		NOTIFY_DOWNLOAD_STARTED,
		NOFITY_DOWNLOAD_IN_PROGRESS,
		NOTIFY_DOWNLOAD_CANCELED,
	};
	void SendNotification(NotificationType type, CefRefPtr<CefBrowser> browser, int percentComplete = -1, CefRefPtr<CefDownloadItemCallback> callback = NULL);

	// Support for downloading files.
	std::string last_download_file_;

	IProgressDialog *progress_dialog_ptr_;
	bool progress_started_, name_selected_;

	// Request that all existing browser windows close.
	void CloseAllBrowsers(bool force_close);

	bool IsClosing() const { return is_closing_; }

private:
	// List of existing browser windows. Only accessed on the CEF UI thread.
	typedef std::list<CefRefPtr<CefBrowser> > BrowserList;
	BrowserList browser_list_;

	bool is_closing_;

	// Returns the full download path for the specified file, or an empty path to
	// use the default temp directory.
	std::string GetDownloadPath(const std::string& file_name);

	// Include the default reference counting implementation.
	IMPLEMENT_REFCOUNTING(SimpleHandler);
};

#endif  // CEF_TESTS_CEFSIMPLE_SIMPLE_HANDLER_H_
