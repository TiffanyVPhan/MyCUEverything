document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('form-submit').addEventListener('click', function () {
        document.getElementById('form').className = 'hide';
        document.getElementById('loader').className = 'loader';
    })
});