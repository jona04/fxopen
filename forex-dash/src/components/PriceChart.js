import React, { useEffect } from 'react'
import { drawChart } from '../app/chart';

function PriceChart({
    priceData,
    selectedPair,
    selectedGranularity,
    selectedCount
}) {

    useEffect(() => {
        if (priceData) {
            console.log("Drwa Chart", selectedPair, selectedGranularity,selectedCount);
            drawChart(priceData, selectedPair, selectedGranularity, 'chartDiv')
        }
    }, [priceData])

    return (
        <div className='segment' id='price-chart-holder'>
            <div id='chartDiv'></div>
        </div>
    )
}

export default PriceChart