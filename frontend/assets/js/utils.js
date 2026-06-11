export function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container fixed bottom-4 right-4 z-50 flex flex-col gap-2';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast p-4 rounded bg-gray-100 border-l-4 shadow-lg flex items-center justify-between min-w-[300px] transform transition-all duration-300 translate-y-full opacity-0`;
  
  if (type === 'success') toast.classList.add('border-success', 'text-white');
  if (type === 'error') toast.classList.add('border-error', 'text-white');
  
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);
  
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-full', 'opacity-0');
  });

  setTimeout(() => {
    toast.classList.add('translate-y-full', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

export function formatPrice(amount) {
  return `₹${parseFloat(amount).toLocaleString('en-IN')}`;
}

export function initNavbarScroll() {
  const nav = document.querySelector('.navbar');
  if (nav) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        nav.classList.add('scrolled', 'bg-black/95', 'backdrop-blur-md');
      } else {
        nav.classList.remove('scrolled', 'bg-black/95', 'backdrop-blur-md');
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initNavbarScroll();
});
