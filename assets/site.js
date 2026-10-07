// Infinity Club — shared behaviour
(function () {
  // Render TeX with KaTeX if it loaded.
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
      throwOnError: false
    });
  }
  // Answers are hidden on screen, always printed.
  var ans = document.querySelector("section.answers");
  if (ans) {
    ans.classList.add("is-hidden");
    var btn = document.createElement("button");
    btn.className = "answers-toggle";
    btn.textContent = "Show answers";
    btn.addEventListener("click", function () {
      var hidden = ans.classList.toggle("is-hidden");
      btn.textContent = hidden ? "Show answers" : "Hide answers";
    });
    ans.parentNode.insertBefore(btn, ans);
  }
  // Print buttons.
  document.querySelectorAll("[data-print]").forEach(function (b) {
    b.addEventListener("click", function () { window.print(); });
  });
})();
