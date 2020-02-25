# DeepBench

### What is it?
Simulation library for very simple simulations to *benchmark* machine learning algorithms.
![Example Image of pipeline](/repository_support/images/DeepSkies_Logos_DeepBench.png) Format: ![Alt Text](url)


### Why do we need it? Why is it useful?
1. There are very universally recognized scientifically meaningful benchmark data sets, or methods with which to generate them.
2. A very simple data set will have objects, patterns, and signals that are intuitively quanitifiable and will be fast to generate.
3. A very simple data set will be a great testing ground for new networks and for newcomers to practice with the technology.


## Requirements
1. python 3.x
2. matplotlib


## General Features
1. very fast to generate
2. Mimics in a very basic / toy way what is in astro images
3. Be fully controllable parametrically


## Example
![Example Image of pipeline](/repository_support/images/example_simplephysicalimage.png) Format: ![Alt Text](url)


## Planned Features
1. Kinds of data to mimic
	1. Strong lenses: Arcs, circles
	2. Supernovae: light curves
	3. Quasars: Skewed Sine wave
	4. N-body simulations: Points in 2D and 3D and in lightcones
	5. Galaxy clusters: Optical - points and 2d kernels; SZ - blurred circles; X-ray - blurred circles
	6. Spectra (stellar, galactic)
	7. Noise: photon, psf
2. Dimensions of data
	1. point / graph
	2. 1D, 2D, 3D, 4D (space-time), 6D (phase space)
	3. Shapes: Polygons, Circles, squares, Polyhedrons, Spheres, cubes
3. Top Data Sets for Initial Release:
	1. Strong lenses
	2. Light curves


## Original Development Team
1. Craig Brechmos
2. Renee Hlozek
3. Brian Nord


## How to contribute
I'm really glad you're reading this, because we need volunteer developers to help this project come to fruition.

### Testing

### Submitting changes

Please send a [GitHub Pull Request to simplephysicaliage](https://github.com/deepskies/SimplePhysicalImage/pull/new/master) with a clear list of what you've done (read more about [pull requests](http://help.github.com/pull-requests/)). When you send a pull request, we will love you forever if you include examples. We can always use more test coverage. Please follow our coding conventions (below) and make sure all of your commits are atomic (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    > 
    > A paragraph describing what changed and its impact."

### Coding conventions

Start reading our code and you'll get the hang of it. We optimize for readability:

  * We indent using tabs
  * We ALWAYS put spaces after list items and method parameters (`[1, 2, 3]`, not `[1,2,3]`), around operators (`x += 1`, not `x+=1`), and around hash arrows.
  * This is open source software. Consider the people who will read your code, and make it look nice for them. It's sort of like driving a car: Perhaps you love doing donuts when you're alone, but with passengers the goal is to make the ride as smooth as possible.
