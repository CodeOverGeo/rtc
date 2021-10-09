const OPEN_MAP_API_KEY = 'e480c0a2-c3be-438b-90ea-db01e1d26c74';
const GOOGLE_MAP_API_KEY = 'AIzaSyDibstff_ItmrGuOHDU9ag28HY5VEcNts8';

let map;
let homeMarker;
let geocoder;
let errorDiv;
let response;
let chargers = [];
let chargerMarker;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: { lat: -34.397, lng: 150.644 },
    mapTypeControl: false,
  });
  geocoder = new google.maps.Geocoder();

  const inputText = document.createElement('input');

  inputText.type = 'text';
  inputText.placeholder = 'Enter a location';

  const submitButton = document.createElement('input');

  submitButton.type = 'button';
  submitButton.value = 'Search';
  submitButton.classList.add('button', 'button-primary');

  const clearButton = document.createElement('input');

  clearButton.type = 'button';
  clearButton.value = 'Clear';
  clearButton.classList.add('button', 'button-secondary');
  response = document.createElement('pre');
  response.id = 'response';
  response.innerText = '';
  errorDiv = document.createElement('div');
  errorDiv.id = 'response-container';
  errorDiv.appendChild(response);

  const instructionsElement = document.createElement('p');

  instructionsElement.id = 'instructions';
  instructionsElement.innerHTML =
    '<strong>Instructions</strong>: Enter an address to search for charging stations.';
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(inputText);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(submitButton);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(clearButton);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(instructionsElement);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(errorDiv);

  homeMarker = new google.maps.Marker({
    map,
  });
  chargerMarker = new google.maps.Marker({
    map,
  });

  map.addListener('click', async (e) => {
    geocode({ location: e.latLng });
  });
  submitButton.addEventListener('click', () =>
    geocode({ address: inputText.value })
  );

  clearButton.addEventListener('click', () => {
    clear();
  });
  clear();
}

function clear() {
  homeMarker.setMap(null);
  chargers = [];
  errorDiv.style.display = 'none';
}

function geocode(request) {
  clear();
  geocoder
    .geocode(request)
    .then((result) => {
      const { results } = result;
      map.setCenter(results[0].geometry.location);
      homeMarker.setPosition(results[0].geometry.location);
      homeMarker.setMap(map);
      return results;
    })
    .then((result) => {
      const results = result;
      const lat = result[0].geometry.location.lat();
      const lng = result[0].geometry.location.lng();
      chargerLookup(lat, lng);
      return results;
    })
    .catch((e) => {
      response.innerText = 'Please enter a valid address';
      errorDiv.style.display = 'block';
    });
}

async function chargerLookup(lat, lng) {
  const res = await axios.get('https://api.openchargemap.io/v3/poi/', {
    params: {
      output: 'json',
      countrycode: 'US',
      maxresults: '10',
      key: OPEN_MAP_API_KEY,
      latitude: lat,
      longitude: lng,
    },
  });
  if (res && res.data) {
    for (let i = 0; i < 10; i++) {
      chargers.push(res.data[i]);
    }
    placeChargerOnMap();
    createChargerCards();
    return chargers;
  }
  return False;
}

function placeChargerOnMap() {
  if (chargers) {
    const image = {
      url: '/static/images/bolt.png',
      scaledSize: new google.maps.Size(25, 25),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(0, 0),
    };

    const shape = { coords: [1, 1, 1, 20, 18, 20, 18, 1], type: 'poly' };

    for (let i = 0; i < chargers.length; i++) {
      const charger = chargers[i].AddressInfo;
      chargerMarker = new google.maps.Marker({
        position: {
          lat: charger.Latitude,
          lng: charger.Longitude,
        },
        map,
        icon: image,
        shape: shape,
        title: charger.Title,
        zIndex: i,
      });
      chargerMarker.setMap(map);
    }
  }
  return chargers;
}

function createChargerCards() {
  console.log('inside');
  for (let i = 0; i < chargers.length; i++) {
    const chargerAddress = chargers[i].AddressInfo;
    const chargerConnection = chargers[i].Connections[0].ConnectionType;
    $('#charger-cards').append(`      
        <div class="col-4">
            <div class="card-columns">'
                <div class="card text-white bg-dark mb-3">
                    <div class="card-body">
                        <h5 class="card-title">${chargerAddress.Title}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">${chargerAddress.AddressLine1}, ${chargerAddress.Town}, ${chargerAddress.StateOrProvince} ${chargerAddress.Postcode}</h6>
                        <p class="card-text">${chargerConnection.FormalName}</p>
                        <a href="#" class="btn btn-primary">Open</a>
                    </div>
                </div>
            </div>
        </div>
        `);
  }
}
