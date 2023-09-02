
function deleteConfirm() {
    let confirmDelete = confirm("Delete book");
    if (confirmDelete) {
        document.getElementById('confirm').value = "yes";
        document.getElementById('form').submit;
    }
}
function issueConfirm() {
    let confirmDelete = confirm("Issue book");
    if (confirmDelete) {
        document.getElementById('confirm').value = "yes";
        document.getElementById('issueForm').submit;
    }
}
