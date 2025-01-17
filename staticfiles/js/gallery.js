document.addEventListener('DOMContentLoaded', () => {
  const viewButtons = document.querySelectorAll('.view-button');
  viewButtons.forEach(button => {
    button.addEventListener('click', () => {
      const view = button.dataset.view;
      const currentURL = new URL(window.location.href);
      const params = new URLSearchParams(currentURL.search);
      params.set('view', view);
      currentURL.search = params.toString();
      window.location.href = currentURL.toString();
    });
  });
});