import React, { useEffect, useState } from 'react'
import { COUNTS } from '../app/data'
import Select from '../components/Select'
import TitleHead from '../components/TitleHead'
import Button from '../components/Button'
import endPoints from '../app/api'
import PriceChart from '../components/PriceChart'

function Dashboard() {

  const [ selectedPair, setSelectedPair ] = useState(null);
  const [ selectedGranularity, setSelectedGranularity ] = useState(null);
  const [ priceData, setPriceData ] = useState(null);
  const [ selectedCount, setSelectedCount ] = useState(COUNTS[0].value);
  const [ options, setOptions ] = useState(null);
  const [ loading, setLoading ] = useState(true);

  useEffect(() => {
    loadOptions();
  }, []);

  const handleCountChange = (count) => {
    setSelectedCount(count);
    loadPricesCandle(count);
  }

  const loadPricesCandle = async (count) => {
    const data = await endPoints.prices_candle(selectedPair, selectedGranularity, count)
    setPriceData(data)
  }

  const loadOptions = async () => {
    const data = await endPoints.options();
    console.log("data",data);
    setOptions(data);
    setSelectedGranularity(data.granularities[0].value);
    setSelectedPair(data.pairs[0].value);
    setLoading(false);
  }

  if (loading === true) return <h1>Loading...</h1>

  return (
    <div>
        <TitleHead title="Options" />
        <div className='segment options'>
            <Select 
                name="Currency"
                title="Select currency"
                options={options.pairs}
                defaultValue={selectedPair}
                onSelected={setSelectedPair}
            />
            <Select 
                name="Granularity"
                title="Select granularity"
                options={options.granularities}
                defaultValue={selectedGranularity}
                onSelected={setSelectedGranularity}
            />
            <Select 
                name="numRows"
                title="Num. Rows."
                options={ COUNTS }
                defaultValue={selectedCount}
                onSelected={handleCountChange}
            />
            {/* <input value={numberCandles} onChange={e => setNumberCandles(e.target.value)} type="number" /> */}
            <Button text="Load" handleClick={() => loadPricesCandle(selectedCount)} />
        </div>
        {/* <TitleHead title="Technicals" />
        { pricesCandle &&  <Technicals data={pricesCandle} /> } */}
        <TitleHead title="Price Chart" />
        { priceData && <PriceChart 
          selectedCount={selectedCount}
          selectedPair={selectedPair}
          selectedGranularity={selectedGranularity}
          handleCountChange={handleCountChange}
          priceData={priceData}
        />}
    </div>
  )
}

export default Dashboard