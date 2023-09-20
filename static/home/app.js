const cityInputField = document.querySelector("#cityInput")
const citySubmitButton = document.querySelector("#citySubmitButton")
const citiesToClick = document.querySelector("#citiesToClick")
let doneTypingInterval = 500;  
let typingTimer;

cityInputField.addEventListener("keyup", (e) => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => {
        if (e.target.value !== null || e.target.value != "") {
            getRequest(e.target.value)
        }
    }, doneTypingInterval);
})


cityInputField.addEventListener("keydown", () => {
    clearTimeout(typingTimer);
})

const getRequest = async (cityName) => {
    const response = await axios.get("/api", {
    params: {
        "city": cityName
    }
    })
    let cities = response.data

    addNewCitiesToDom(cities)
}

function addNewCitiesToDom(cities) {
    citiesToClick.innerHTML = ""
    cities.forEach(city => {
        let cityNode = document.createElement("li")
        cityNode.classList.add("city")
        let cityName = document.createElement("span")
        cityName.appendChild(document.createTextNode(city.name))
        let iso = document.createElement("span")
        iso.classList.add("iso")
        iso.appendChild(document.createTextNode(" - " + city.iso))
        cityNode.appendChild(cityName)
        cityNode.appendChild(iso)
        citiesToClick.appendChild(cityNode)
        cityName.addEventListener("click", (e) => {
            submitCityForm(e.target.innerHTML);
        })
    });
}

function submitCityForm(cityName) {
    cityInputField.style.visibility = "hidden"
    cityInputField.value = cityName
    citySubmitButton.click()
}   
