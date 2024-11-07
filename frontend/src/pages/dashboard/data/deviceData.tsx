import { LuRefrigerator } from 'react-icons/lu'
import { GiClothes, GiChickenOven } from 'react-icons/gi'
import { TbIroning3 } from 'react-icons/tb'
import { HiOutlineDesktopComputer } from 'react-icons/hi'
import { FaPlaystation } from 'react-icons/fa'
import { PiTelevisionSimple } from 'react-icons/pi'
import { AiFillSound } from 'react-icons/ai'

export const deviceData = [
  {
    id: 1,
    name: 'Refrigerador',
    icon: <LuRefrigerator />,
    color: '#4793AF',
  },
  {
    id: 2,
    name: 'Lavadora',
    icon: <GiClothes />,
    color: '#FFC470',
  },
  {
    id: 3,
    name: 'Plancha de Ropa',
    icon: <TbIroning3 />,
    color: '#DD5746',
  },
  {
    id: 4,
    name: 'Computadora',
    icon: <HiOutlineDesktopComputer />,
    color: '#8B322C',
  },
  {
    id: 5,
    name: 'Horno',
    icon: <GiChickenOven />,
    color: '#FA7070',
  },
  {
    id: 6,
    name: 'Consola de Juegos',
    icon: <FaPlaystation />,
    color: '#59D5E0',
  },
  {
    id: 7,
    name: 'Televisión',
    icon: <PiTelevisionSimple />,
    color: '#C6EBC5',
  },
  {
    id: 8,
    name: 'Sistema de Sonido',
    icon: <AiFillSound />,
    color: '#A1C398',
  },
]
