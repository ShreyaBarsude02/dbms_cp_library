function deleteConfirm() {
  let confirmDelete = confirm("Delete book");
  if (confirmDelete) {
    document.getElementById("confirm").value = "yes";
    document.getElementById("form").submit;
  }
}
function issueConfirm() {
  let confirmIssue = confirm("Issue book");
  if (confirmIssue) {
    document.getElementById("confirm").value = "yes";
    document.getElementById("issueForm").submit;
  }
}

function returnConfirm(){
  let confirmReturn = confirm("Return");
  if (confirmReturn) {
    document.getElementById("confirm").value = "yes";
    document.getElementById("returnform").submit;
  }
}

function goBack() {
  // Using the history object to go back to the previous page
  window.history.back();
}

function closeAlert() {
  var alert = document.querySelector('.alert');
  alert.style.display = 'none';
}
