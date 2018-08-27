let currentPage = 1
let isCurrentlyLoadingNextPage = false
let hasMorePhotosToLoad = true
let isShowingSearch = false
let searchParameter
const IMAGE_CONTAINER_BOOTSTRAP_CLASS = 'col-4' // multiple of 12
const endlessFooterAuxiliaryElement = document.querySelector('.footer-endless-scroll')
const loadingElement = document.querySelector('#loading')
const noImagesToShow = document.querySelector('#no-images')
const searchInputText = document.getElementById('search_input_text')
const searchInputDate = document.getElementById('search_input_date')
const locationSelect = document.getElementById('location')
// DOM element to display the images
let $images = document.getElementById('images')

const init = () => {
    fetchImages()
    initEndlessScrollEvent()
    initSearchEvents()
    fetchLocations()
}

const fetchImages = () => {
    showLoading()
    let API_URL = '/api/feed?page=' + currentPage
    if (isShowingSearch) {
        API_URL = '/api/search?' + searchParameter + '&page=' + currentPage
    }
    if (currentPage === 1) {
        hasMorePhotosToLoad = true
    }
    fetch(API_URL).then(response => {
        response.json().then(data => {
            hideLoading()
            hideMessageNoImagesToShow()
            console.log(data)
            fillImages(data)
            isCurrentlyLoadingNextPage = false
            if (data.length === 0) {
                hasMorePhotosToLoad = false
                if (currentPage === 1) {
                    showMessageNoImagesToShow()
                }
            }
        })
    })
}

const emptyImages = () => {
    // empty its contents
    while ($images.firstChild) {
        $images.removeChild($images.firstChild)
    }
}

const fillImages = images => {
    // for each image
    images.map(image => {
        let imageUrl = image.image_aws_url

        // create an <img>
        let $image = document.createElement('img')
        $image.setAttribute('src', imageUrl)
        if (image.caption && image.caption.text) {
            $image.setAttribute('title', image.caption.text)
        }

        // create an <a>
        let $hyperlink = document.createElement('a')
        $hyperlink.setAttribute('href', imageUrl)
        $hyperlink.setAttribute('target', '_blank')
        // append the image to the hyperlink
        $hyperlink.appendChild($image)

        // create a <div> for details
        let $details = document.createElement('div')
        $details.setAttribute('class', 'details')
        // username
        let $username = document.createElement('a')
        $username.setAttribute('class', 'username')
        $username.setAttribute('href', 'http://instagram.com/' + image.user.username)
        $username.setAttribute('target', '_blank')
        $username.textContent = '👠 @' + image.user.username
        $details.appendChild($username)
        // instagram link
        if (image.source === 'feed') {
            let $br = document.createElement('br')
            $details.appendChild($br)
            let $instagramLink = document.createElement('a')
            $instagramLink.setAttribute('href', 'http://instagram.com/p/' + image.code)
            $instagramLink.setAttribute('target', '_blank')
            $instagramLink.textContent = '📸 Ver no Instagram'
            $details.appendChild($instagramLink)
        }
        // taken at
        if (image.taken_at) {
            let $br2 = document.createElement('br')
            $details.appendChild($br2)
            let $takenAt = document.createElement('span')
            $takenAt.textContent = '📅 ' + new Date(image.taken_at * 1000).toLocaleString()
            $details.appendChild($takenAt)
        }
        // likes & comments
        if (image.comment_count || image.like_count) {
            let $likesComments = document.createElement('div')
            $likesComments.textContent = '🖤 ' + image.like_count + ' / 💬 ' + image.comment_count
            $details.appendChild($likesComments)
        } else {
            let $storyComments = document.createElement('div')
            $storyComments.textContent = '⌛ (story)'
            $details.appendChild($storyComments)
        }
        // location
        if (image.location && image.location.name) {
            let $location = document.createElement('div')
            $location.textContent = '📍' + image.location.name
            $details.appendChild($location)
        }
        // remove image
        let $removeImage = document.createElement('div')
        $removeImage.className = 'cursor_pointer'
        $removeImage.textContent = '❌ Remover foto'
        $removeImage.onclick = e => { removePhoto(image.id, e) }
        $details.appendChild($removeImage)
        // add tags
        let $addTags = document.createElement('div')
        $addTags.className = 'cursor_pointer'
        $addTags.textContent = '➕ Adicionar tags customizadas'
        $addTags.onclick = e => { addTags(image.id, e) }
        $details.appendChild($addTags)
        // create a container
        let $imageContainer = document.createElement('div')
        $imageContainer.setAttribute('class', IMAGE_CONTAINER_BOOTSTRAP_CLASS)
        // append the hyperlink and the image to the container
        $imageContainer.appendChild($hyperlink)
        // append the details
        $imageContainer.appendChild($details)
        // append it to DOM
        $images.appendChild($imageContainer)
    })
}

const onNextPage = e => {
    currentPage++
    console.log('Loading page', currentPage)
    fetchImages()
}

const initEndlessScrollEvent = () => {
    window.onscroll = e => {
        let endlessFooterPosition = endlessFooterAuxiliaryElement.getBoundingClientRect()
        if (!isCurrentlyLoadingNextPage && hasMorePhotosToLoad) {
            if (endlessFooterPosition.y - window.pageYOffset < 300) {
                isCurrentlyLoadingNextPage = true
                onNextPage()
            }
        }
    }
}

const showLoading = () => {
    loadingElement.className = ''
}

const hideLoading = () => {
    loadingElement.className = 'hidden'
}

const showMessageNoImagesToShow = () => {
    noImagesToShow.className = ''
}

const hideMessageNoImagesToShow = () => {
    noImagesToShow.className = 'hidden'
}

const initSearchEvents = () => {
    document.getElementById('search_option').onchange = changeSearchOption
    document.getElementById('do_search').onclick = doSearch
    document.getElementById('clear_search').onclick = clearSearch
    document.getElementById('search_input_text').onkeyup = e => {
        e.preventDefault()
        if (e.keyCode === 13) {
            doSearch()
        }
    }
}

const changeSearchOption = e => {
    let searchOption = document.getElementById('search_option').value
    if (searchOption === 'date') {
        locationSelect.className = 'hidden'
        searchInputDate.className = ''
        searchInputText.className = 'hidden'
    } else if (searchOption === 'location') {
        locationSelect.className = ''
        searchInputDate.className = 'hidden'
        searchInputText.className = 'hidden'
    } else {
        locationSelect.className = 'hidden'
        searchInputDate.className = 'hidden'
        searchInputText.className = ''
    }
}

const doSearch = e => {
    let searchOption = document.getElementById('search_option').value
    if (searchOption === 'date') {
        let startDate = document.querySelector('#start_date').value
        let endDate = document.querySelector('#end_date').value
        if (startDate === '' || endDate === '') {
            alert('É preciso escolher uma data inicial e final para realizar a busca.')
            return false
        }
        callSearchAPI('start_date=' + getUnixDate(startDate) + '&end_date=' + getUnixDate(endDate))
    } else if (searchOption === 'location') {
        let location = document.getElementById('location').value
        callSearchAPI('location=' + location)
    } else {
        let searchValue = searchInputText.value
        
        // treat empty values
        if (searchValue === '') {
            alert('É preciso digitar um valor para fazer a busca.')
            return false
        }

        // specific treatments
        if (searchOption === 'username') {
            // remove @
            searchValue = searchValue.replace('@', '')
        } else if (searchOption === 'hashtags') {
            searchValue = searchValue.replace(/#/g, '').split(' ').map(t => '%23' + t).join('|')
        } else if (searchOption === 'custom_tags') {
            searchValue = searchValue.split(',').map(t => t.trim()).join('|')
        }
        callSearchAPI(searchOption + '=' + searchValue)
    }
    if (e) {
        e.preventDefault()
    }
    return false
}

const getUnixDate = dateString => {
    if (dateString === '') {
        return null
    }
    let dateArray = dateString.split('-').map(s => parseInt(s, 10))
    let dateObj = new Date(dateArray[0], dateArray[1] - 1, dateArray[2])
    return (+dateObj)/1000
}

const callSearchAPI = endpoint => {
    console.log(endpoint)
    emptyImages()
    isShowingSearch = true
    searchParameter = endpoint
    currentPage = 1
    fetchImages()
}

const clearSearch = e => {
    searchInputText.value = ''
    locationSelect.value = ''
    emptyImages()
    isShowingSearch = false
    searchParameter = null
    currentPage = 1
    fetchImages()
    e.preventDefault()
    return false
}

const removePhoto = (photoId, e) => {
    if (window.confirm('Tem certeza que deseja excluir esta foto?')) {
        fetch('/api/exclude/' + photoId, {
            method: 'put',
        }).then(data => {
            console.log(data)
            e.target.parentElement.parentElement.remove()
        })
    }
}

const addTags = (photoId, e) => {
    let tags = window.prompt('Entre tags para foto, separando por vírgula (por ex: sandália, salto fino):')
    console.log(tags, e)
    if (tags) {
        tags = tags.split(',')
        console.log(tags)
        tags = tags.map(tag => tag.trim())
        console.log(tags)
        tags = tags.join(',')
        console.log(tags)
        fetch('/api/custom_tags/' + photoId + '?tags=' + tags, {
            method: 'put',
        }).then(data => {
            console.log(data)
        })
    }
}

const fetchLocations = () => {
    fetch('/api/locations').then(response => {
        response.json().then(locations => {
            locations.sort().map(location => {
                let option = document.createElement('option')
                option.setAttribute('value', location)
                option.textContent = location
                locationSelect.appendChild(option)
            })
        })
    })
}

init()
