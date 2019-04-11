# Front End

This is the documentation and notes for the front end.

## Overview

The front end is built on React, and it is primarly written in Javascript and HTML. The front end uses the Material UI library to build the user interface.

  
## Components

## Routing
App.js contains the routing information for the front end. '/' is the root and displays the graph.
# Notes for React

## How to install React on MacOS
1. Install Node.js

```
brew install node
or
https://nodejs.org/en/
```

2. Install create-react-app package

```
npm i -g create-react-app
```

3. Create React App

```
create-react-app web-ui
```

4. Start React app

```
cd web-ui
npm start
```

5. Go to localhost

## How to push branch to origin
1. Fetch new, if any, changes from origin

```
git fetch origin
```

2. Rebase local branch with remote

```
git rebase origin/react_app
```

3. Push branch

```
git push origin react_app
```

### Other

1. Show files in commit

```
git diff --name-only HEAD~1 HEAD
```

# Run npm install in directory with package.json

# Testing

1. Install Enyzme

```
npm install --save-dev enzyme enzyme-adapter-react-16 enzyme-to-json
```

2. Run tests

```
npm tests
```

# Material UI

```
npm install @material-ui/core
```

```
npm install ajv
```

# React Routing

```
npm install --save react-router-dom
```
