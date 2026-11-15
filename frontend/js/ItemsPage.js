document.addEventListener("DOMContentLoaded", () => {
    const categorySelect = document.getElementById("category");
    if (!categorySelect) return;

    categorySelect.addEventListener("change", () => {
        const category = categorySelect.value;
        const itemType = window.location.pathname.startsWith("/item/found") ? "found" : "lost";
        const endpoint = `/item/${itemType}`;
        window.location.href = categorySelect.value
            ? `${endpoint}/${encodeURIComponent(categorySelect.value)}`
            : endpoint;
    });
});
