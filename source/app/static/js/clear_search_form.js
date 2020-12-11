function clear_search_form(textsFieldId, checkboxsFieldName) {
    textsFieldId.forEach(each => document.getElementById(each).value = "");
    checkboxsFieldName
        .forEach(checkboxFieldName => document.getElementsByName(checkboxFieldName)
            .forEach(checkbox => checkbox.checked = false));
        
}
