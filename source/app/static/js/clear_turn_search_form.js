function clear_turn_search_form(textsFieldId, selectedFieldId) {
  textsFieldId.forEach((each) => (document.getElementById(each).value = ""));
  selectedFieldId.forEach(
    (each) =>
      (document.getElementById(each).value =
        "Elija alguno de los siguientes emails")
  );
}
