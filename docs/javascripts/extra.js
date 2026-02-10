document.addEventListener("DOMContentLoaded", () => {
  if (window.mermaid) {
    window.mermaid.initialize({ startOnLoad: true });
    window.mermaid.init(undefined, document.querySelectorAll(".mermaid"));
  }
});
