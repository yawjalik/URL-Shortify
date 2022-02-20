import Head from 'next/head'
import Image from 'next/image'
import { useState } from 'react'
import { toast } from 'react-toastify'
import NavBar from '../components/navbar'
import axios from 'axios'

export default function Home() {
  const [text, setText] = useState("")
  const [hash, setHash] = useState("")
  const [loading, setLoading] = useState(false)

  const onClick = (e) => {
    if (text.length > 0) {
      setLoading(true)
      axios.post(`http://localhost:8000/shorten`, {url: text})
        .then(res => {
          // console.log(res.data.data.shortened_url)
          setHash(res.data.data.shortened_url)
          setText("")
          setLoading(false)
        })
        .catch(err => {
          // console.log(err)
          setLoading(false)
          toast.error("Invalid URL or something else went wrong")
          setHash("")
        })
    }
  }

  return (
    <div className='text-center'>
      <h1 className='text-4xl font-bold my-2'>URL Shortify</h1>
      <NavBar/>
      <input className='bg-gray-200 rounded px-2 py-1 m-2' type="text" placeholder='Enter URL to shorten' value={text} onChange={e => setText(e.target.value)}/>
      <button disabled={loading} className="bg-blue-200 hover:bg-blue-300 rounded px-2 py-1 m-2" onClick={onClick}>
        {loading ? "Loading" : "Shorten"}
      </button>

      <h2 className='text-2xl my-4'>
        <a className='text-blue-500' href={hash} target='_blank'>{hash}</a>
      </h2>
    </div>
  )
}