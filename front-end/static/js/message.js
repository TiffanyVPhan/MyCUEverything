document.addEventListener('DOMContentLoaded', function () {
    if (window.location.href.split('?')[1] === 'error') {
        document.getElementById('alert').className = 'red';
        document.getElementById('alert-text').innerText = 'Invalid login credentials.';
    }
    else if (window.location.href.split('?')[1] === 'logout') {
        document.getElementById('alert').className = 'green';
        document.getElementById('alert-text').innerText = 'Successfully logged out.';
    }
    window.history.pushState('/', 'MyCUEverything', '/');
});
