(function () {
  const fileInput = document.getElementById("fileInput");
  const dropzone = document.getElementById("dropzone");
  const fileMeta = document.getElementById("fileMeta");
  const emailText = document.getElementById("emailText");
  const charCount = document.getElementById("charCount");
  const loading = document.getElementById("loading");
  const submitBtn = document.getElementById("submitBtn");
  const form = document.getElementById("emailForm");

  const copyBtn = document.getElementById("copyBtn");
  const clearBtn = document.getElementById("clearBtn");

  function updateCharCount() {
    if (!charCount || !emailText) return;
    charCount.textContent = `${emailText.value.length.toLocaleString()} chars`;
  }
  updateCharCount();
  emailText?.addEventListener("input", updateCharCount);

  function showFileMeta(file) {
    if (!fileMeta) return;
    if (!file) { fileMeta.textContent = ""; return; }
    fileMeta.textContent = `Arquivo: ${file.name} (${Math.round(file.size / 1024)} KB)`;
  }

  fileInput?.addEventListener("change", (e) => {
    const f = e.target.files?.[0];
    showFileMeta(f);
  });

  // Drag & drop UX
  if (dropzone && fileInput) {
    ["dragenter", "dragover"].forEach(evt =>
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add("dragover");
      })
    );

    ["dragleave", "drop"].forEach(evt =>
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove("dragover");
      })
    );

    dropzone.addEventListener("drop", (e) => {
      const f = e.dataTransfer.files?.[0];
      if (!f) return;
      fileInput.files = e.dataTransfer.files;
      showFileMeta(f);
    });
  }

  form?.addEventListener("submit", () => {
    loading?.classList.remove("d-none");
    submitBtn?.setAttribute("disabled", "disabled");
  });

  copyBtn?.addEventListener("click", async () => {
    const pre = document.querySelector(".reply-box pre");
    if (!pre) return;
    await navigator.clipboard.writeText(pre.textContent);
    copyBtn.textContent = "Copiado ✅";
    setTimeout(() => (copyBtn.textContent = "Copiar resposta"), 1200);
  });

  clearBtn?.addEventListener("click", () => {
    window.location.href = "/";
  });
})();
