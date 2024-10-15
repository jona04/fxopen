import React, { useEffect } from 'react'
import { drawChart } from '../app/chart';

function PriceChart({
    priceData,
    selectedPair,
    selectedGranularity,
    indicatorData
}) {

    useEffect(() => {
        if (indicatorData) {
            console.log("indicator price chart");
            drawChart(indicatorData, selectedPair, selectedGranularity, 'chartDiv', indicatorData)
        } else {
            console.log("aqui novamente");
            drawChart(priceData, selectedPair, selectedGranularity, 'chartDiv', null)
        }
    }, [priceData, indicatorData])

    return (
        <div className='segment' id='price-chart-holder'>
            <div id='chartDiv'></div>
        </div>
    )
}

export default PriceChart