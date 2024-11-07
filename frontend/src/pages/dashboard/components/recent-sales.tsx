import { deviceData } from "../data/deviceData";

export function RecentSales() {
  return (
    <div className='flex flex-col space-y-4'>
      {deviceData.map((device) => (
        <div key={device.id} className='flex items-start'>
          <div className='h-9 w-9 flex-none'>{device.icon}</div>
          <div className='ml-4 flex-grow'>
            <p className='text-sm font-medium leading-none'>{device.name}</p>
          </div>
          <div className='ml-4 flex-none'>
            <div
              className='h-9 w-9 rounded-full'
              style={{ backgroundColor: device.color }}
            ></div>
          </div>
          <div className='ml-2 flex-none'>
            <p className='text-sm font-medium leading-none'>{device.color}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
