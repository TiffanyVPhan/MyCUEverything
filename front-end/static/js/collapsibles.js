document.addEventListener('DOMContentLoaded', function () {
    let elements = document.querySelectorAll('.collapsible');
    for (const element of elements) {
        M.Collapsible.init(element, {});
    }
});