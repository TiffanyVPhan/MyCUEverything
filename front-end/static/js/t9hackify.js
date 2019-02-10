function t9Hackify() {
    for (const element of document.querySelectorAll('*')){
        element.className = element.className + ' purple';
    }
}