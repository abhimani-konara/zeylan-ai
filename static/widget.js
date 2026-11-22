(function () {
  var script = document.currentScript;
  var base = script ? new URL(script.src).origin : "http://127.0.0.1:8000";
  var isOpen = false;

  var btn = document.createElement("button");
  btn.textContent = "Chat";
  btn.setAttribute("aria-label", "Open Zeylan AI chat");
  btn.style.cssText = "position:fixed;right:20px;bottom:20px;z-index:2147483000;width:64px;height:64px;border-radius:50%;border:0;background:#0f766e;color:#fff;font-size:14px;font-weight:bold;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.3);";

  var frame = document.createElement("iframe");
  frame.title = "Zeylan AI chat";
  frame.style.cssText = "position:fixed;right:20px;bottom:96px;z-index:2147483000;width:380px;height:560px;max-width:calc(100vw - 24px);max-height:calc(100vh - 120px);border:1px solid #d1d5db;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.25);background:#fff;display:none;";

  btn.addEventListener("click", function () {
    isOpen = !isOpen;
    if (isOpen && !frame.src) { frame.src = base + "/static/chat.html"; }
    frame.style.display = isOpen ? "block" : "none";
    btn.textContent = isOpen ? "Close" : "Chat";
  });

  document.body.appendChild(frame);
  document.body.appendChild(btn);
})();
