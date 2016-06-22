import os
import random
import string
import sys

from optparse import OptionParser

def error(code):
    errors = {0:'Error in application, check to ensure axl is up-to-date and configured properly',
              1:'Error in path specification, check permissions and ensure path is not empty',
              2:'Error in seed specification, ensure seed is not empty and does not contain slashes'}

    sys.exit('Exited application with ERROR ' + str(code) + ': ' + errors[code])

def cli():
    parser = OptionParser()
    parser.add_option('--path',
                      action='store',
                      dest='path',
                      metavar='str',
                      help='path of desired directory to export web extension package')
    parser.add_option('--seed',
                      action='store',
                      dest='seed',
                      metavar='str',
                      help='custom name for web extension (default: axl followed by a random six-character alphanumeric code)')
    options, args = parser.parse_args()

    print 'Options,', parser.parse_args()

    generate(opt_path=options.path, opt_seed=options.seed)

def generate(opt_path=None, opt_seed=None):
    path = opt_path
    seed = opt_seed

    if path is None:
        path = os.getcwd()

    print 'Path,', path

    if path[len(path)-1] != '/':
        path += '/'
    path += 'webext/'

    if not os.path.exists(path):
        os.makedirs(path)

    if seed is None:
        seed = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    print 'Seed,', seed

    ext_name = 'axl' + str(seed)
    print 'Name generated, ' + ext_name
    ext_id = 'axl' + str(seed) + '@mozilla.org'
    print 'ID generated, ' + ext_id

    print 'Creating manifest...'
    manifest = open(path + 'manifest.json', 'w')
    print 'Manifest path: ' + path + 'manifest.json'
    manifest.write('{"manifest_version": 2, "name": "' + ext_name + '", "version": "1.0", "description": "Aides in efforts to improve automation testing in Firefox Add-ons.", "applications": { "gecko": { "id": "' + ext_id + '", "strict_min_version": "45.0" } }, "content_scripts": [ { "matches": ["*://justinpotts.github.io/project-axl-frontend/test?key=' + ext_name + '"], "js": ["genext.js"] } ] } ')
    manifest.close()
    print 'Manifest created'

    print 'Creating JS...'
    genextjs = open(path + 'genext.js', 'w')
    print 'JS path: ' + path + 'genext.js'
    genextjs.write('document.getElementById(\'indicator\').innerHTML = \'<p><img id="success" src="media/img/check-mark.jpg"></p><p><span class="download-completion">It works!</span></p><p><span class="install-instructions">To disable or remove the add-on, visit about:addons.</span></p>\';')
    genextjs.close()
    print 'JS created'

    package_successful = package(path, ext_name)
    if not package_successful:
        error(0)

    cleanup_successful,xpi_path = cleanup(path, ext_name)
    if cleanup_successful:
        print 'Success! Extension .xpi generated at:', xpi_path
    else:
        error(0)

def package(path, ext_name):
    print 'Packaging extension...'
    os.chdir(path)
    print os.getcwd()
    print 'Name: ' + ext_name
    os.system('zip -r ../' + ext_name + '.xpi *')
    print 'Extension packaged in .xpi at ' + path + ext_name + '.xpi'
    os.chdir('../')
    print 'Cleaning up...'
    return True

def cleanup(path, ext_name):
    os.chdir(path)
    os.system('rm manifest.json')
    os.system('rm genext.js')
    os.chdir('..')
    os.system('rm -rf webext/')

    xpi_path = path[:len(path)-7]

    return (True, xpi_path + ext_name + '.xpi')


if __name__ == '__main__':
    cli()
