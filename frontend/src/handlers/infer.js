import axios from 'axios'

export const inferHandler = async (obj) => {
    console.log(obj)
    const url = "http://stark-woodland-02229.herokuapp.com/predict"
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    }
    const response = await axios.post(url, obj, config)
    console.log(response)
    return Math.round(response.data.grade)
}