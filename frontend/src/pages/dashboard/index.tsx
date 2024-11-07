/* eslint-disable @typescript-eslint/no-explicit-any */
import { Button } from '@/components/custom/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import ThemeSwitch from '@/components/theme-switch'
import { UserNav } from '@/components/user-nav'
import { Layout, LayoutBody, LayoutHeader } from '@/components/custom/layout'
import { RecentSales } from './components/recent-sales'
import { createChart } from 'lightweight-charts'
import { seriesData } from './data/series-data'
import { useRef, useEffect, useState } from 'react'
import { deviceData } from './data/deviceData'
import * as d3 from 'd3'

export default function Dashboard() {
  // Use useRef to get a reference to the container element
  const chartContainerRef = useRef(null)
  const pieChartRef = useRef(null) // Referencia para el contenedor del gráfico de pastel
  const chart = useRef(null) // This will store the chart instance
  const [consummedWatts, setConsummedWatts] = useState(0)
  const [houseType, setHouseType] = useState('Casa')
  const [address, setAddress] = useState('Calle 123 #123')
  const [devices, setDevices] = useState(8)

  useEffect(() => {
    const width = window.innerWidth
    setConsummedWatts(573)
    setHouseType('Apartamento')
    setAddress('Calle 123 #123')
    setDevices(8)
    // This condition ensures the chart is only created once
    if (chart.current === null) {
      if (chartContainerRef.current !== null) {
        chart.current = createChart(chartContainerRef.current, {
          width: width * 0.75,
          height: 300,
          rightPriceScale: {
            scaleMargins: {
              top: 0.2,
              bottom: 0.1,
            },
          },
          leftPriceScale: {
            visible: true,
          },
          timeScale: {
            rightOffset: 20,
          },
        }) as any
      }

      if (chart.current !== null) {
        const lineSeries = (chart.current as any).addLineSeries({
          color: deviceData[0].color,
        })
        lineSeries.setData(seriesData)
        const lineSeries2 = (chart.current as any).addLineSeries({
          color: deviceData[1].color,
        })
        lineSeries2.setData([
          { time: '2019-04-11', value: 22.01 },
          { time: '2019-04-12', value: 24.63 },
          { time: '2019-04-13', value: 23.64 },
          { time: '2019-04-14', value: 22.89 },
          { time: '2019-04-15', value: 22.43 },
          { time: '2019-04-16', value: 25.01 },
          { time: '2019-04-17', value: 22.63 },
          { time: '2019-04-18', value: 26.64 },
          { time: '2019-04-19', value: 24.89 },
          { time: '2019-04-20', value: 22.43 },
        ])
      }
    }

    // Cleanup function to avoid memory leaks
    return () => {
      if (chart.current !== null) {
        (chart.current as any).remove()
      }
      chart.current = null
    }
  }, [])

  useEffect(() => {
    const renderPieChart = () => {
      const data = [10, 20, 30] // Example data
      const color = d3.scaleOrdinal(deviceData.map((d) => d.color)) // Use colors from deviceData

      const width = 400
      const height = 400
      const outerRadius = height / 2 - 10
      const innerRadius = outerRadius * 0.75

      let svg: any = d3.select(pieChartRef.current).select('svg')

      // Check if the SVG already exists
      if (svg.empty()) {
        // Create SVG element if it doesn't exist
        svg = d3
          .select(pieChartRef.current)
          .append('svg')
          .attr('width', width)
          .attr('height', height)
          .append('g')
          .attr('transform', `translate(${width / 2}, ${height / 2})`)
      } else {
        // Clear the previous content
        svg.selectAll('*').remove()
      }

      const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius)
      const pie = d3
        .pie()
        .sort(null)
        .value((d: any) => d)

      // Bind the data to the paths and enter + update
      svg
        .selectAll('path')
        .data(pie(data))
        .enter()
        .append('path')
        .merge(svg.selectAll('path')) // Merge enter and update selections
        .attr('d', (d: any) => arc(d) as string) // Add type assertion to fix the problem
        .attr('fill', (_: any, i: any) => color(i))
    }

    // Call renderPieChart to create or update the chart
    renderPieChart()

    // Cleanup function to remove the SVG when the component unmounts
    return () => {
      d3.select(pieChartRef.current).select('svg').remove()
    }
  }, [])

  return (
    <Layout>
      {/* ===== Top Heading ===== */}
      <LayoutHeader>
        <div className='ml-auto flex items-center space-x-4'>
          <ThemeSwitch />
          <UserNav />
        </div>
      </LayoutHeader>

      {/* ===== Main ===== */}
      <LayoutBody className='space-y-4'>
        <div className='flex items-center justify-between space-y-2'>
          <h1 className='text-2xl font-bold tracking-tight md:text-3xl'>
            Dashboard
          </h1>
          <div className='flex items-center space-x-2'>
            <Button>Descargar</Button>
          </div>
        </div>
        <Tabs
          orientation='vertical'
          defaultValue='overview'
          className='space-y-4'
        >
          <div className='w-full overflow-x-scroll pb-2'>
            <TabsList>
              <TabsTrigger value='overview'>Overview</TabsTrigger>
              <TabsTrigger value='analytics'>Analytics</TabsTrigger>
              <TabsTrigger value='reports'>Reports</TabsTrigger>
              <TabsTrigger value='notifications'>Notifications</TabsTrigger>
            </TabsList>
          </div>
          <TabsContent value='overview' className='space-y-4'>
            <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-4'>
                  <CardTitle className='text-sm font-medium'>
                    Watts consumidos
                  </CardTitle>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox='0 0 24 24'
                    fill='none'
                    stroke='currentColor'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth='2'
                    className='h-4 w-4 text-muted-foreground'
                  >
                    <path d='M22 12h-4l-3 9L9 3l-3 9H2' />
                  </svg>
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>{consummedWatts}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-4'>
                  <CardTitle className='text-sm font-medium'>
                    Tipo de Casa
                  </CardTitle>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox='0 0 24 24'
                    fill='none'
                    stroke='currentColor'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth='2'
                    className='h-4 w-4 text-muted-foreground'
                  >
                    <path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2' />
                    <circle cx='9' cy='7' r='4' />
                    <path d='M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75' />
                  </svg>
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>{houseType}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-4'>
                  <CardTitle className='text-sm font-medium'>
                    Dirección
                  </CardTitle>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox='0 0 24 24'
                    fill='none'
                    stroke='currentColor'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth='2'
                    className='h-4 w-4 text-muted-foreground'
                  >
                    <rect width='20' height='14' x='2' y='5' rx='2' />
                    <path d='M2 10h20' />
                  </svg>
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>{address}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-4'>
                  <CardTitle className='text-sm font-medium'>
                    Dispositivos Conectados
                  </CardTitle>
                  <svg
                    xmlns='http://www.w3.org/2000/svg'
                    viewBox='0 0 24 24'
                    fill='none'
                    stroke='currentColor'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                    strokeWidth='2'
                    className='h-4 w-4 text-muted-foreground'
                  >
                    <path d='M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6' />
                  </svg>
                </CardHeader>
                <CardContent>
                  <div className='text-2xl font-bold'>{devices}</div>
                </CardContent>
              </Card>
            </div>
            <div className='grid grid-cols-1 gap-4 lg:grid-cols-7'>
              <Card className='col-span-1 lg:col-span-4'>
                <CardHeader>
                  <CardTitle>Overview</CardTitle>
                </CardHeader>
                <CardContent className='pl-2'>
                  <div
                    ref={pieChartRef}
                    style={{
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center',
                    }}
                  />
                </CardContent>
              </Card>
              <Card className='col-span-1 lg:col-span-3'>
                <CardHeader>
                  <CardTitle>Dispositivos</CardTitle>
                  <CardDescription>
                    Los colores asociados a los dispositivos son:
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <RecentSales />
                </CardContent>
              </Card>
            </div>
            <Card className='col-span-1 lg:col-span-4'>
              <div ref={chartContainerRef} />
            </Card>
          </TabsContent>
        </Tabs>
      </LayoutBody>
    </Layout>
  )
}
