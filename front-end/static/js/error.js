document.addEventListener('DOMContentLoaded', function () {
    if (window.location.href.split('?')[1] === 'error') {
        document.getElementById('error').className = 'red-text';
    }
});
