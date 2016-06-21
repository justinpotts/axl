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
                      default=os.getcwd(),
                      metavar='str',
                      help='path of desired directory to export web extension package')
    '''
    parser.add_option('--seed',
                      action='store',
                      dest='seed',
                      default='test',
                      metavar='str',
                      help='custom name for web extension (default: axl followed by a random six-character alphanumeric code)')
    '''
    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        parser.exit()

    generate(opt_path=options.path, opt_seed=options.path)

def generate(opt_path=None, opt_seed=None):
    path = opt_path
    seed = str(opt_seed)

    if opt_path is None:
        path = os.getcwd()
        print 'Path generated,', path
    else:
        print 'Path found,', path

    if path[len(path)-1] != '/':
        path += '/'
    path += 'webext/'

    if not os.path.exists(path):
        os.makedirs(path)

    if seed is None:
        seed = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
        print 'Seed generated,', seed
    else:
        print 'Seed found,', seed

    ext_name = 'axl' + seed
    print 'Name generated, ' + ext_name
    ext_id = 'axl' + seed + '@mozilla.org'
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

    os.chdir(path)
    print 'Packaging extension...'
    os.system('zip -r ../' + ext_name + '.xpi *')
    print 'Extension packaged in .xpi at ' + path + ext_name + '.xpi'
    os.chdir('../')
    print 'Cleaning up...'

    os.chdir('webext/')
    os.system('rm manifest.json')
    os.system('rm genext.js')
    os.chdir('..')
    os.system('rm -rf webext/')

    xpi_path = path[:len(path)-7]

    print 'Success! Web extension at ' + xpi_path + ext_name + '.xpi'

    return xpi_path + ext_name + '.xpi'

if __name__ == '__main__':
    cli()
