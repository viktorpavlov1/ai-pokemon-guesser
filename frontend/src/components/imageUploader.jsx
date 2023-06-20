import * as React from 'react';
import './imageUploader.css';

function ImageUploader() {

    const [image, setImage] = React.useState(null);
    const [type, setType] = React.useState(null);
    const [pokemon, setPokemon] = React.useState(null);

    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
    }

    const handleGuessTypeSubmit = (e) => {
        e.preventDefault();

        if (image) {
            const formData = new FormData();
            formData.append('file', image);

            fetch('http://localhost:5000/pokemon/type/guess', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    setType(data.prediction);
                    console.log(data);
                })
                .catch(err => {
                    console.log(err);
                })
        }
    }

    const handleGuessPokemonSubmit = (e) => {
        e.preventDefault();
    
        if (image) {
          const formData = new FormData();
          formData.append('file', image);
    
          fetch('http://localhost:5000/pokemon/guess', {
            method: 'POST',
            body: formData
          })
            .then(res => res.json())
            .then(data => {
              setPokemon(data.prediction);
              console.log(data);
            })
            .catch(err => {
              console.log(err);
            })
        }
      }

    return (
        <div className="image-uploader">
            <form className='poke-form'>
            <div className='left-side'>
                {image && <img src={URL.createObjectURL(image)} alt='pokemon' />}
                <input className='image-input' type="file" accept='image/*' onChange={handleImageChange} />
            </div>
            <div className='right-side'>
                {pokemon && <h1 className='guessed-pokemon'>The guessed pokemon is: {pokemon}</h1>}
                {type && <h1 className='guessed-type'>The type of this pokemon is: {type}</h1>}
                <div className='pok-buttons'>
                <button className='type-btn' type='submit' onClick={handleGuessTypeSubmit}>Guess Type</button>
                <button className='pokemon-btn' type='submit' onClick={handleGuessPokemonSubmit}>Guess Pokemon</button>
                </div>
            </div>
            </form>
        </div>
    );
}

export default ImageUploader;