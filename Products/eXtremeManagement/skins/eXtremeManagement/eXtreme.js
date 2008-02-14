/* Functions for toggling visibility of elements */

function toggle_display(id) {
    var element = document.getElementById(id);
    if (element.style.display == 'none') {
        element.style.display = '';
    } else {
        element.style.display = 'none';
    }
}

function toggle_border(number) {
    var header = document.getElementById('toggle-header-' + number);
    var item = document.getElementById('toggle-item-' + number);
    if (item.style.display == 'none') {
	header.cells[0].className = header.cells[0].className.replace(/ clear-bottom/, '');
    } else {
	header.cells[0].className = header.cells[0].className + ' clear-bottom';
    }
}

function toggle_item(number) {
    toggle_display('toggle-item-' + number);
    toggle_border(number);
}
