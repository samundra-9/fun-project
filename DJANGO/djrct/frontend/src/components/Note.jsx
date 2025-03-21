 
export default function Note({ note, onDelete }) {
    const formattedDate = new Date(note.created_at).toLocaleDateString('en-US');
    return (
        <div key={note.id} className="bg-white p-6 rounded-lg shadow-md mt-4">
            <h1 className="text-xl font-semibold text-gray-700">{note.title}</h1>
            <p className="text-gray-600 mt-2">{note.content}</p>
            <p className="text-gray-500 mt-2">{formattedDate}</p>
            <button
                onClick={() => onDelete(note.id)}
                className="bg-red-500 text-white py-1 px-2 rounded-md mt-4 hover:bg-red-600 transition duration-200"
            >
                Delete
            </button>
        </div>
    );
}
