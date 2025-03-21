 import React, { use, useEffect } from 'react'
 import api from '../api'
import Note from '../components/Note'
 
 export default function Home() {
  const [notes, setNotes] = React.useState([])
  const [content, setContent] = React.useState('')
  const [title, setTitle] = React.useState('')

  const getNotes = async () => {
    api.get('/api/notes/')
    .then((res) => res.data)
    .then((data) => setNotes(data))
    .catch((error) => alert(error))
  } 
  const deleteNotes = async (id) => {
    api.delete(`/api/notes/delete/${id}`)
    .then((res) => {
      if(res.status === 204){
        alert('Note deleted')
      }
      else{
        alert('Failed to delete note')
      }
    })
    .catch((error) => alert(error))
    getNotes() 
  };

  const createNotes = async (e) => {
    e.preventDefault();
    api.post('/api/notes/',{
      title,
      content
    })
    .then((res) => {
      if(res.status === 201){
        alert('Note created')
       
      }
      else{
        alert('Failed to create note')
      }
    })
    .catch((error) => alert(error))
    getNotes()
  }

  useEffect(() => {
    getNotes()
  }
  ,[])
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800">Notes</h1>
        {
          notes.map((note) => (
            <Note key={note.id} note={note} onDelete={deleteNotes} />
          ))
        }
      </div>
      <div className="max-w-lg mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-2xl font-semibold text-gray-700 mb-4">Create a Note</h1>
        <form onSubmit={createNotes} className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-600">
              Title:
            </label>
            <input
              type="text"
              id="title"
              value={title}
              required
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Title"
              className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:ring focus:ring-blue-300 focus:outline-none"
            />
          </div>
          <div>
            <label htmlFor="content" className="block text-sm font-medium text-gray-600">
              Content:
            </label>
            <textarea
              id="content"
              value={content}
              required
              onChange={(e) => setContent(e.target.value)}
              placeholder="Content"
              className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:ring focus:ring-blue-300 focus:outline-none"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition duration-200"
          >
            Create Note
          </button>
        </form>
      </div>
    </div>
  )
 }
 