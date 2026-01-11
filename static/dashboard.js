document.addEventListener("DOMContentLoaded", function () {
    const visualBtn = document.getElementById("visual");
    const metricBtn = document.getElementById("metric");
    const summaryBtn = document.getElementById("summary");

    const visualSection = document.getElementById("visual-section");
    const metricsSection = document.getElementById("metrics-section");
    const summarySection = document.getElementById("summary-section");

    function activate(activeBtn) {
        [visualBtn, metricBtn, summaryBtn].forEach(btn => {
            if (btn) btn.classList.remove("active");
        });
        activeBtn.classList.add("active");
    }

    visualBtn?.addEventListener("click", function (e) {
        e.preventDefault();
        visualSection.style.display = "block";
        metricsSection.style.display = "none";
        if (summarySection) summarySection.style.display = "none";
        activate(visualBtn);
    });

    metricBtn?.addEventListener("click", function (e) {
        e.preventDefault();
        visualSection.style.display = "none";
        metricsSection.style.display = "block";
        if (summarySection) summarySection.style.display = "none";
        activate(metricBtn);
    });

    summaryBtn?.addEventListener("click", function (e) {
        e.preventDefault();
        visualSection.style.display = "none";
        metricsSection.style.display = "none";
        if (summarySection) summarySection.style.display = "block";
        activate(summaryBtn);
    });
});
