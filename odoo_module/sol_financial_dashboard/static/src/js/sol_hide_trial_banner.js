/** @odoo-module **/
/*
 * Cosmetic only: hide the Odoo.sh trial-project expiration banner.
 *
 * The CSS covers the standard expiration-panel classes; this JS is a
 * text-based fallback for the Odoo.sh trial banner whose exact markup can
 * vary. It runs a few times shortly after load (the banner renders after the
 * web client boots) — no perpetual observer, so no runtime cost afterwards.
 *
 * This changes nothing about the trial itself: the database remains unbacked
 * and scheduled for automatic deletion until the Odoo.sh project is upgraded
 * to a paid plan.
 */
function solHideTrialBanner() {
    document
        .querySelectorAll(".o_database_expiration_panel, .database_expiration_panel, .o_expiration_panel")
        .forEach((el) => el.remove());
    // Fallback: only scan lightweight alert containers for the trial wording.
    document.querySelectorAll(".alert, .o_notification_content").forEach((el) => {
        const text = (el.textContent || "").toLowerCase();
        if (text.includes("odoo.sh") && text.includes("trial")) {
            const box = el.closest(".alert") || el;
            box.remove();
        }
    });
}

[0, 400, 1200, 3000].forEach((delay) => setTimeout(solHideTrialBanner, delay));
