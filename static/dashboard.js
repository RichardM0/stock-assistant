document.addEventListener("DOMContentLoaded", function () {
    const visualBtn = document.getElementById("visual");
    const metricBtn = document.getElementById("metric");
    const compareBtn = document.getElementById("compare");
    const summaryBtn = document.getElementById("summary");

    const visualSection = document.getElementById("visual-section");
    const metricsSection = document.getElementById("metrics-section");
    const compareSection = document.getElementById("compare-section");
    const summarySection = document.getElementById("summary-section");

    function hideAll() {
        visualSection.style.display = "none";
        metricsSection.style.display = "none";
        compareSection.style.display = "none";
        summarySection.style.display = "none";
    }

    function activate(activeBtn) {
        [visualBtn, metricBtn, compareBtn, summaryBtn].forEach(btn => {
            if (btn) btn.classList.remove("active");
        });
        activeBtn.classList.add("active");
    }

    function setActiveTab(tabName) {
        localStorage.setItem("activeTab", tabName);
    }

    visualBtn?.addEventListener("click", function (e) {
        e.preventDefault();
        hideAll();
        visualSection.style.display = "block";
        activate(visualBtn);
        setActiveTab("visual");
    });

    metricBtn?.addEventListener("click", function (e) {
        e.preventDefault();
        hideAll();
        metricsSection.style.display = "block";
        activate(metricBtn);
        setActiveTab("metrics");
    });

    compareBtn?.addEventListener("click", function (e) {
        e.preventDefault();
        hideAll();
        compareSection.style.display = "block";
        activate(compareBtn);
        setActiveTab("compare");
    });

    summaryBtn?.addEventListener("click", function (e) {
        e.preventDefault();
        hideAll();
        summarySection.style.display = "block";
        activate(summaryBtn);
        setActiveTab("summary");
    });

    const savedTab = localStorage.getItem("activeTab");

    switch (savedTab) {
        case "metrics":
            metricBtn?.click();
            break;
        case "compare":
            compareBtn?.click();
            break;
        case "summary":
            summaryBtn?.click();
            break;
        default:
            visualBtn?.click();
    }
});

