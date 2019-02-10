let chart = document.getElementById('gpatrend').getContext('2d');

Chart.defaults.global.defaultFontFamily = 'Arial';
Chart.defaults.global.defaultFontSize = 18;
Chart.defaults.global.defaultFontColor = 'black';

let gpa_trend = document.currentScript.getAttribute('gpatrend').split(',');
gpa_trend.pop();
let gpa_trend_no_zero = [];
for (const i in gpa_trend) {
    gpa_trend_no_zero.push(gpa_trend[i]);
    if (gpa_trend_no_zero[i] === '0' && i !== '0') gpa_trend[i] = gpa_trend[i-1]
}

new Chart(chart, {
    type: 'bar',
    data: {
        labels: gpa_trend,
        datasets: [{
            label: 'Cumulative',
            backgroundColor: 'black',
            data: gpa_trend,
            type: 'line',
            borderColor: 'black',
            fill: false
        }, {
            label: 'Term',
            data: gpa_trend_no_zero,
            backgroundColor: '#CFB87C',
            borderWidth: 1,
            borderColor: '#777',
            hoverBorderWidth: 3,
            hoverBorderColor: '#000'
        }
        ]
    },
    options: {
        title: {
            display: true,
            text: '',
            fontSize: 25
        },
        legend: {
            display: true,
            position: 'right',
            labels: {
                fontColor: '#000'
            }
        },
        layout: {
            padding: {
                left: 50,
                right: 0,
                bottom: 0,
                top: 0
            }
        },
        tooltips: {
            enabled: true
        }
    }
});