"use strict";
(() => {
  // Components are optional; removing a whole module must not break the page.
  document.querySelectorAll('[role="tablist"]').forEach(list => {
    const tabs = [...list.querySelectorAll('[role="tab"]')];
    const activate = target => {
      tabs.forEach(tab => {
        const active = tab === target, panel = document.getElementById(tab.getAttribute("aria-controls"));
        tab.setAttribute("aria-selected", String(active)); tab.tabIndex = active ? 0 : -1;
        if (panel) { panel.hidden = !active; if (!active) panel.querySelectorAll("video").forEach(v => v.pause()); }
      });
      document.dispatchEvent(new Event("scenechange"));
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => activate(tab));
      tab.addEventListener("keydown", event => {
        const choices = {ArrowRight: (index + 1) % tabs.length, ArrowLeft: (index + tabs.length - 1) % tabs.length, Home: 0, End: tabs.length - 1};
        if (!(event.key in choices)) return;
        event.preventDefault(); const next = tabs[choices[event.key]]; activate(next); next.focus();
      });
    });
    if (tabs.length) activate(tabs.find(tab => tab.getAttribute("aria-selected") === "true") || tabs[0]);
  });
  const dialog = document.getElementById("figure-dialog");
  if (dialog) {
    const image = dialog.querySelector("img"), area = dialog.querySelector(".dialog-image-area"), zoom = dialog.querySelector("[data-zoom]");
    document.querySelectorAll("[data-lightbox]").forEach(link => link.addEventListener("click", event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || !dialog.showModal) return;
      const source = link.querySelector("img"); if (!source) return;
      event.preventDefault(); image.src = link.href; image.alt = source.alt;
      dialog.querySelector("#figure-title").textContent = source.alt;
      dialog.querySelector("[data-original]").href = link.href;
      area.classList.remove("is-zoomed"); area.scrollTop = 0; area.scrollLeft = 0;
      zoom.setAttribute("aria-pressed", "false"); zoom.textContent = "Actual size"; dialog.showModal();
    }));
    zoom.addEventListener("click", () => { const full = area.classList.toggle("is-zoomed"); zoom.setAttribute("aria-pressed", String(full)); zoom.textContent = full ? "Fit to window" : "Actual size"; });
    dialog.querySelector("[data-close]").addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", e => { if (e.target === dialog) dialog.close(); });
  }
  document.querySelectorAll("[data-copy]").forEach(button => button.addEventListener("click", async () => {
    const code = document.getElementById(button.dataset.copy), status = button.closest("section").querySelector("[data-copy-status]");
    if (!code) return;
    try { await navigator.clipboard.writeText(code.textContent); if (status) status.textContent = "BibTeX copied."; }
    catch { const range = document.createRange(); range.selectNodeContents(code); const selection = getSelection(); selection.removeAllRanges(); selection.addRange(range); if (status) status.textContent = "Citation selected. Press Ctrl+C or Command+C to copy."; }
  }));
  document.querySelectorAll("[data-image-compare]").forEach(component => {
    const stage = component.querySelector(".compare-stage"), handle = component.querySelector(".compare-handle");
    const images = [...component.querySelectorAll("img")], status = component.querySelector('[role="status"]');
    if (!stage || !handle || images.length !== 2) return;
    let position = 50, dragging = false;
    const set = value => {
      position = Math.max(0, Math.min(100, value)); stage.style.setProperty("--position", position + "%");
      handle.setAttribute("aria-valuenow", String(Math.round(position)));
      handle.setAttribute("aria-valuetext", Math.round(position) + "% " + (component.dataset.leftLabel || "left image"));
    };
    const point = event => { const box = stage.getBoundingClientRect(); if (box.width) set((event.clientX - box.left) / box.width * 100); };
    stage.addEventListener("pointerdown", e => { if (e.button !== 0) return; dragging = true; stage.setPointerCapture(e.pointerId); point(e); });
    stage.addEventListener("pointermove", e => { if (dragging) point(e); });
    ["pointerup", "pointercancel", "lostpointercapture"].forEach(type => stage.addEventListener(type, () => { dragging = false; }));
    handle.addEventListener("keydown", e => {
      const values = {ArrowLeft: position - 5, ArrowRight: position + 5, Home: 0, End: 100};
      if (e.key in values) { e.preventDefault(); set(values[e.key]); }
    });
    const inspect = () => {
      if (!images.every(img => img.complete && img.naturalWidth)) return;
      const mismatch = Math.abs(images[0].naturalWidth / images[0].naturalHeight - images[1].naturalWidth / images[1].naturalHeight) > 0.001;
      component.classList.toggle("compare-invalid", mismatch);
      if (status) status.textContent = mismatch ? "Comparison images have different aspect ratios; showing both images separately." : "";
    };
    images.forEach(img => { img.addEventListener("load", inspect); img.addEventListener("error", () => { if (status) status.textContent = "An image could not be loaded."; }); });
    set(50); inspect();
  });
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (!entry.isIntersecting) entry.target.pause(); }), {threshold: .1});
    // Dynamic comparisons observe their visible container, not the hidden decoding video.
    document.querySelectorAll("video").forEach(video => { if (!video.closest("[data-video-comparison]")) observer.observe(video); });
  }
  document.addEventListener("visibilitychange", () => { if (document.hidden) document.querySelectorAll("video").forEach(video => video.pause()); });
})();
