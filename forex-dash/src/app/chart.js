import Plotly from 'plotly.js-dist';

export function drawChart(chartData, p, g, divName) {
    let trace = {
        x: chartData.time,
        close: chartData.mid_c,
        high: chartData.mid_h,
        low: chartData.mid_l,
        open: chartData.mid_o,
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y',
        increasing: { line: { width: 1, color: '#24A06B'}, fillColor: "#24A06B" },
        decreasing: { line: { width: 1, color: '#CC2E3C'}, fillColor: "#CC2E3C" }          
    }

    let data = [trace]

    let layout = {
        title: `Data for ${p} ${g}`,
        heigh: '100%',
        autosize: true,
        showlegend: false,
        margin: {
            l: 50, r:50, b:50, t:50
        },
        xaxis: {
            rangeslider: {
                visible: false
            }
        }
    };

    Plotly.newPlot(divName, data, layout, { responsive: true });
    Plotly.Plots.resize(document.getElementById(divName));


}