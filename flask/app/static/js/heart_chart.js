document.addEventListener("DOMContentLoaded", function() {
    var canvas = document.getElementById("heartActivityChart");
    if (!canvas) {
        console.error("⚠️ Canvas element 'heartActivityChart' nebyl nalezen!");
        return;
    }

    var dataElement = document.getElementById("heart-data");
    if (!dataElement) {
        console.warn("⚠️ Žádná data pro graf.");
        return;
    }

    try {
        var jsonData = JSON.parse(dataElement.textContent);
        var casove_razitka = jsonData.casove_razitka;
        var hodnoty_srdce = jsonData.hodnoty_srdce;
        var cviceni_hodnoty = jsonData.cviceni_hodnoty;

        if (casove_razitka.length === 0 || hodnoty_srdce.length === 0) {
            console.warn("⚠️ Načteno prázdné pole pro graf.");
            return;
        }

        var ctx = canvas.getContext("2d");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: casove_razitka,
                datasets: [{
                    label: "Srdeční aktivita (BPM)",
                    data: hodnoty_srdce,
                    borderColor: "red",
                    fill: false,
                    tension: 0.3,
                    pointRadius: 5,  // Zvýraznění bodů
                    pointHoverRadius: 8, // Zvětšení bodů při najetí
                    pointBackgroundColor: function(context) {
                        var cviceni = cviceni_hodnoty[context.dataIndex];
                        return cviceni === 0 ? "gray" : 
                               cviceni === 1 ? "blue" : 
                               cviceni === 2 ? "orange" : "red";
                    }
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: "top"
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                var index = tooltipItem.dataIndex;
                                var cviceni = cviceni_hodnoty[index];
                                var cviceni_text = cviceni === 0 ? "Žádná aktivita" : 
                                                   cviceni === 1 ? "Lehká aktivita" : 
                                                   cviceni === 2 ? "Střední aktivita" : 
                                                   "Intenzivní aktivita";
                                return `BPM: ${tooltipItem.raw}, Aktivita: ${cviceni_text}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Čas"
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Hodnota BPM"
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("🚨 Chyba při načítání dat grafu:", error);
    }
});