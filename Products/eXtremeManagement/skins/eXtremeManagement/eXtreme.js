/* Functions for toggling visibility of elements */

function toggle_display(id) {
    var element = document.getElementById(id);
    if (element.style.display == 'none') {
        element.style.display = '';
    } else {
        element.style.display = 'none';
    }
    
}

function toggle_item(number) {
    toggle_display('toggle-item-' + number);
}
