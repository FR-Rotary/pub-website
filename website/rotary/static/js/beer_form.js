document.addEventListener("DOMContentLoaded", () => {
  const element = document.getElementById('country-select');
  console.log(element)
  const choices = new Choices(element, {
    searchEnabled: true,
    renderChoiceLimit: 3,
    searchResultLimit: 3,
    closeDropdownOnSelect: true,
  });
});
