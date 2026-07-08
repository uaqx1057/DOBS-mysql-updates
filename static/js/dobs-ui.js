/*
 * DOBS UI — one shared module replacing the five incompatible modal APIs,
 * eight+ duplicated search-filter functions, and ad hoc alert()/confirm()
 * calls that existed across the old per-page inline <script> blocks.
 *
 * Markup contract (data-attributes, not inline onclick=""):
 *   Modal:   <button data-modal-open="driverModal">...
 *            <div class="modal" id="driverModal">
 *              <button data-modal-close>...
 *   Tabs:    <div data-tabs>
 *              <button data-tab="onboarding" class="tab-btn active">...
 *            <div data-tab-panel="onboarding" class="tab-panel">...
 *   Filter:  <input data-filter-cards="#onboardingTab .driver-card">
 *            (matches against each card's data-search attribute if present,
 *            else its visible textContent)
 *   Reveal:  add class "reveal" to any element; IntersectionObserver adds
 *            "is-visible" with a stagger based on DOM order among siblings.
 *   Count-up: <span data-count-to="42">0</span>
 *
 * Page/section cross-fade transitions are handled declaratively via
 * <meta name="view-transition" content="same-origin"> in base.html - no JS
 * needed for that; browsers without support simply navigate normally.
 */
(function () {
  "use strict";

  // ---------------------------------------------------------------------
  // Modals
  // ---------------------------------------------------------------------
  function openModal(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.add("show");
    document.dispatchEvent(new CustomEvent("dobs:modal-open", { detail: { id } }));
  }

  function closeModal(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove("show");
    document.dispatchEvent(new CustomEvent("dobs:modal-close", { detail: { id } }));
  }

  function closeAllModals() {
    document.querySelectorAll(".modal.show").forEach((m) => m.classList.remove("show"));
  }

  function initModals() {
    document.addEventListener("click", (e) => {
      const openTrigger = e.target.closest("[data-modal-open]");
      if (openTrigger) {
        openModal(openTrigger.getAttribute("data-modal-open"));
        return;
      }
      const closeTrigger = e.target.closest("[data-modal-close]");
      if (closeTrigger) {
        const modal = closeTrigger.closest(".modal");
        if (modal) closeModal(modal.id);
        return;
      }
      // Click on the backdrop itself (not its content) closes it.
      if (e.target.classList.contains("modal") && e.target.classList.contains("show")) {
        e.target.classList.remove("show");
      }
    });

    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeAllModals();
    });
  }

  // ---------------------------------------------------------------------
  // Tabs
  // ---------------------------------------------------------------------
  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach((group) => {
      const buttons = group.querySelectorAll("[data-tab]");
      buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
          const target = btn.getAttribute("data-tab");
          buttons.forEach((b) => b.classList.toggle("active", b === btn));
          document.querySelectorAll(`[data-tab-panel]`).forEach((panel) => {
            const isMatch = panel.getAttribute("data-tab-panel") === target;
            panel.hidden = !isMatch;
            if (isMatch) panel.classList.add("tab-panel");
          });
          document.dispatchEvent(new CustomEvent("dobs:tab-change", { detail: { target } }));
        });
      });
    });
  }

  // ---------------------------------------------------------------------
  // Card search/filter (replaces filterOnboardedDrivers/filterOffboarding-
  // Drivers/filterUsers/globalSearchFilter/etc. - one implementation)
  // ---------------------------------------------------------------------
  function initCardFilters() {
    document.querySelectorAll("[data-filter-cards]").forEach((input) => {
      const selector = input.getAttribute("data-filter-cards");
      input.addEventListener("input", () => {
        const term = input.value.trim().toLowerCase();
        document.querySelectorAll(selector).forEach((card) => {
          const haystack = (card.getAttribute("data-search") || card.textContent || "").toLowerCase();
          card.style.display = haystack.includes(term) ? "" : "none";
        });
      });
    });
  }

  // ---------------------------------------------------------------------
  // Toasts (replaces alert()/confirm() success-path notifications)
  // ---------------------------------------------------------------------
  function ensureToastStack() {
    let stack = document.querySelector(".toast-stack");
    if (!stack) {
      stack = document.createElement("div");
      stack.className = "toast-stack";
      document.body.appendChild(stack);
    }
    return stack;
  }

  function toast(message, type = "info", duration = 4000) {
    const stack = ensureToastStack();
    const el = document.createElement("div");
    el.className = `toast-dobs ${type}`;
    el.textContent = message;
    el.addEventListener("click", () => el.remove());
    stack.appendChild(el);
    setTimeout(() => {
      el.style.transition = "opacity var(--duration-base) var(--ease-standard)";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 300);
    }, duration);
  }

  // ---------------------------------------------------------------------
  // Reveal-on-load / reveal-on-scroll
  // ---------------------------------------------------------------------
  function initReveal() {
    const targets = document.querySelectorAll(".reveal");
    if (!targets.length) return;

    if (!("IntersectionObserver" in window)) {
      targets.forEach((el) => el.classList.add("is-visible"));
      return;
    }

    const groups = new Map();
    targets.forEach((el) => {
      const parent = el.parentElement;
      const siblings = groups.get(parent) || [];
      siblings.push(el);
      groups.set(parent, siblings);
    });
    groups.forEach((siblings) => {
      siblings.forEach((el, i) => {
        el.style.transitionDelay = Math.min(i * 40, 400) + "ms";
      });
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    targets.forEach((el) => observer.observe(el));
  }

  // ---------------------------------------------------------------------
  // Count-up stat tiles
  // ---------------------------------------------------------------------
  function countUp(el, target, duration = 900) {
    const start = performance.now();
    const from = 0;
    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(from + (target - from) * eased).toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString();
    }
    requestAnimationFrame(tick);
  }

  function initCountUp() {
    const targets = document.querySelectorAll("[data-count-to]");
    if (!targets.length) return;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    targets.forEach((el) => {
      const target = parseInt(el.getAttribute("data-count-to"), 10) || 0;
      if (reduceMotion || !("IntersectionObserver" in window)) {
        el.textContent = target.toLocaleString();
        return;
      }
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              countUp(el, target);
              observer.unobserve(el);
            }
          });
        },
        { threshold: 0.3 }
      );
      observer.observe(el);
    });
  }

  // ---------------------------------------------------------------------
  // App shell: sidebar collapse/expand (desktop) + off-canvas (mobile)
  // ---------------------------------------------------------------------
  var SIDEBAR_KEY = "dobs:sidebar-collapsed";

  function initSidebar() {
    var shell = document.getElementById("appShell");
    if (!shell) return;

    var collapseBtn = shell.querySelector("[data-sidebar-collapse]");
    var mobileToggle = document.querySelector("[data-sidebar-toggle-mobile]");
    var overlay = shell.querySelector("[data-sidebar-overlay]");

    try {
      if (localStorage.getItem(SIDEBAR_KEY) === "1") {
        shell.setAttribute("data-sidebar-state", "collapsed");
      }
    } catch (e) { /* localStorage unavailable — ignore, default stays expanded */ }

    if (collapseBtn) {
      collapseBtn.addEventListener("click", function () {
        var collapsed = shell.getAttribute("data-sidebar-state") === "collapsed";
        shell.setAttribute("data-sidebar-state", collapsed ? "expanded" : "collapsed");
        try { localStorage.setItem(SIDEBAR_KEY, collapsed ? "0" : "1"); } catch (e) { /* ignore */ }
      });
    }

    function openMobile() {
      shell.setAttribute("data-mobile-open", "true");
      document.body.classList.add("no-scroll");
    }
    function closeMobile() {
      shell.removeAttribute("data-mobile-open");
      document.body.classList.remove("no-scroll");
    }

    if (mobileToggle) {
      mobileToggle.addEventListener("click", function () {
        if (shell.getAttribute("data-mobile-open") === "true") closeMobile();
        else openMobile();
      });
    }
    if (overlay) overlay.addEventListener("click", closeMobile);

    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMobile();
    });

    // Collapsing to a single link on navigation (mobile) keeps the overlay
    // from lingering behind the next page during the view-transition.
    shell.querySelectorAll(".sidebar-nav-item").forEach(function (link) {
      link.addEventListener("click", closeMobile);
    });
  }

  // ---------------------------------------------------------------------
  // Topbar user menu (avatar dropdown)
  // ---------------------------------------------------------------------
  function initUserMenu() {
    var menu = document.querySelector("[data-user-menu]");
    if (!menu) return;
    var toggleBtn = menu.querySelector("[data-user-menu-toggle]");
    if (!toggleBtn) return;

    function close() {
      menu.removeAttribute("data-open");
      toggleBtn.setAttribute("aria-expanded", "false");
    }
    function open() {
      menu.setAttribute("data-open", "true");
      toggleBtn.setAttribute("aria-expanded", "true");
    }

    toggleBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (menu.getAttribute("data-open") === "true") close();
      else open();
    });

    document.addEventListener("click", function (e) {
      if (menu.getAttribute("data-open") === "true" && !menu.contains(e.target)) close();
    });

    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  // ---------------------------------------------------------------------
  // CSRF auto-inject (folds in what used to be includes/csrf_auto.html)
  // ---------------------------------------------------------------------
  function initCsrfAutoInject() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    const token = meta ? meta.content : null;
    if (!token) return;

    document.querySelectorAll("form").forEach((form) => {
      if ((form.getAttribute("method") || "").toLowerCase() !== "post") return;
      if (form.querySelector('input[name="csrf_token"]')) return;
      const input = document.createElement("input");
      input.type = "hidden";
      input.name = "csrf_token";
      input.value = token;
      form.appendChild(input);
    });
  }

  // ---------------------------------------------------------------------
  // Boot
  // ---------------------------------------------------------------------
  document.addEventListener("DOMContentLoaded", () => {
    initModals();
    initTabs();
    initCardFilters();
    initReveal();
    initCountUp();
    initCsrfAutoInject();
    initSidebar();
    initUserMenu();
  });

  // ---------------------------------------------------------------------
  // Business/platform-ID picker (shared by the driver edit modal and the
  // Ops Supervisor dashboard). A single event listener per "Add" button -
  // the old per-page implementations attached this twice in one file,
  // causing every click to add two rows instead of one.
  // ---------------------------------------------------------------------
  function initBusinessPicker(container, addButton, allBusinesses) {
    function addRow(selectedBusinessId, selectedIds) {
      const row = document.createElement("div");
      row.className = "d-flex gap-2 align-items-start mb-2 business-picker-row";

      const businessSelect = document.createElement("select");
      businessSelect.className = "form-select";
      businessSelect.innerHTML =
        '<option value="">Select business…</option>' +
        allBusinesses.map((b) => `<option value="${b.id}">${b.name}</option>`).join("");

      const idsSelect = document.createElement("select");
      idsSelect.className = "form-select";
      idsSelect.name = "platform_id[]";
      idsSelect.multiple = true;

      function populateIds(businessId) {
        const business = allBusinesses.find((b) => String(b.id) === String(businessId));
        idsSelect.innerHTML = "";
        (business ? business.available_ids : []).forEach((idObj) => {
          const opt = document.createElement("option");
          opt.value = idObj.id;
          opt.textContent = idObj.value;
          idsSelect.appendChild(opt);
        });
      }

      businessSelect.addEventListener("change", () => populateIds(businessSelect.value));

      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "btn btn-outline-danger btn-sm";
      removeBtn.textContent = "✕";
      removeBtn.addEventListener("click", () => row.remove());

      row.appendChild(businessSelect);
      row.appendChild(idsSelect);
      row.appendChild(removeBtn);
      container.appendChild(row);

      if (selectedBusinessId) {
        businessSelect.value = selectedBusinessId;
        populateIds(selectedBusinessId);
        if (selectedIds) {
          Array.from(idsSelect.options).forEach((opt) => {
            if (selectedIds.map(String).includes(String(opt.value))) opt.selected = true;
          });
        }
      }
    }

    addButton.addEventListener("click", () => addRow());
    return { addRow, clear: () => { container.innerHTML = ""; } };
  }

  window.DobsUI = { openModal, closeModal, closeAllModals, toast, countUp, initBusinessPicker };
})();
