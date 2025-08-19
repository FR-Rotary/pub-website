document.addEventListener("DOMContentLoaded", () => {
  const element = document.getElementById('country-select');
  const choices = new Choices(element, {
    searchEnabled: true,
    renderChoiceLimit: 3,
    searchResultLimit: 3,
    closeDropdownOnSelect: true,
  });
});
