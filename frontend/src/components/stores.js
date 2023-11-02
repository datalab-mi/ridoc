import { writable, derived } from 'svelte/store';

// authentification
const visitor = {role:"visitor", jwToken:null, rules: ["visitor"], resources:[]}
const dictKeyInclude = (dic1, dic2) => Object.keys(dic1).every(v => Object.keys(dic2).includes(v))

async function testToken(user, set) {
  const response = await fetch(`/backend/authorized_resource`, {
    headers: new Headers({'Authorization'  : `Bearer ${user.jwToken}`})
    });
  console.log(response)
  if (response.ok) {
    set(user)
    list_logger.concat({level: "success", message:  `Connecté en tant que ${user.role}`, ressource: "login"})
  }
  else {
    const response = await fetch(`/backend/authorized_resource/visitor`)
    const data = await response.json()
    set(data)
    //list_logger.concat({level: "success", message: "Connecté en tant que visiteur", ressource: "login"})
  }
}

function createUser(user) {
  // test if user has enough keys
  user = dictKeyInclude(visitor, user) ? user : visitor
  const { subscribe, set, update } = writable(user, () => testToken(user, set))
  return {
    subscribe,
    authenticate: (user) => {
      set(user)
      localStorage.setItem('user', JSON.stringify(user))
    },
    clean: async () => {
      localStorage.removeItem('user')
      const response = await fetch(`/backend/authorized_resource/visitor`)
      const data = await response.json()
      set(data)
      localStorage.setItem('user', JSON.stringify(data))
    },
    updateKey: (key, value) => {
      update(user => user.key = value)
    },
    unauthenticate: async () =>  {
      const response = await fetch(`/backend/authorized_resource/visitor`)
      const data = await response.json()
      set(data)
    },
    refresh: () => testToken(JSON.parse(localStorage.getItem("user")) || visitor, set)
  }
}

export let user
if(typeof window !== "undefined") {
    user = createUser(JSON.parse(localStorage.getItem("user")) || visitor);
} else {
    user = createUser(visitor);
}

export const displayLogin = writable(false)
export const displaysurvey = writable(false)
export const displayComment = writable(false)
export const displayRate = writable(false)

export const headers = derived(user,  $user => {Authorization: `JWT ${$user.jwToken}`})


// logger
const inital_logger_list = [{level: "error",message: "erreur grave", ressource: "authentification", status:401},
        {level: "info",message: "document telechargé", ressource: "upload", status:200}]
// custom store for the logger, every 10 seconds lost first element (the oldest)
function createLogger() {
	const { subscribe, set, update } = writable([], () => {
	const interval = setInterval(() => {
		update(n => n.slice(1, n.length))
	}, 10000);	return () => console.log('no more subscribers');
});
	return {
		subscribe,
		concat: (x) => update(n => JSON.stringify(n.at(-1)) === JSON.stringify(x) ? n : n.concat(x)),
		filter: (msg, key) => update(n => n.filter(t => t[key] !== msg)),
    delete: () => update(n => n.slice(1, n.length)),
		reset: () => set(inital_logger_list)
	};
}

export const list_logger = createLogger();
