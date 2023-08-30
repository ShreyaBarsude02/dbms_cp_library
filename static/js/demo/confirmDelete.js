
function deleteConfirm() {
    let confirmDelete = confirm("Delete book");
    if (confirmDelete) {
        document.getElementById('confirm').value = "yes";
        document.getElementById('form').submit;
    }
}
