if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/assets/service-worker.js")
    .then(reg => console.log("Service worker registered:", reg))
    .catch(err => console.log("SW registration failed:", err));
}
