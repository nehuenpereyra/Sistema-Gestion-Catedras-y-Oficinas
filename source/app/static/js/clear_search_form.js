function clear_search_form(
  textsFieldId,
  checkboxsFieldName,
  selectsFieldName,
  selectsMultipleFieldName
) {
  textsFieldId.forEach((each) => (document.getElementById(each).value = ""));
  checkboxsFieldName.forEach((checkboxFieldName) =>
    document
      .getElementsByName(checkboxFieldName)
      .forEach((checkbox) => (checkbox.checked = false))
  );
  selectsMultipleFieldName.forEach(
    (each) => (document.getElementById(each).selectedIndex = -1)
  );
  selectsFieldName.forEach(
    (each) => (document.getElementById(each).selectedIndex = 0)
  );
}
