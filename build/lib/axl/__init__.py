import os
import random
import string
import sys

def error(code):
    errors = {0:'Error in application, check to ensure axl is up-to-date and configured properly',
              1:'Error in path specification, check permissions and ensure path is not empty',
              2:'Error in seed specification, ensure seed is not empty and does not contain slashes'}

    sys.exit('ERROR ' + str(code) + ': ' + errors[code])

def generate(**keyword_parameters):
    path = ''
    if 'path' in keyword_parameters:
        path = keyword_parameters['path'].strip()
        print 'Path parameter found, ', path
    else:
        try:
            path = sys.argv[1]
        except:
            error(1)

    if path is None or path.strip() == '':
        error(1)

    if path[len(path)-1] != '/':
        path += '/'
    path += 'webext/'

    print 'Generating keys...'
    if 'seed' in keyword_parameters:
        seed = keyword_parameters['seed'].strip()
        if seed is None or seed == '' or '/' in seed:
            error(2)
        else:
            ext_key = seed
            print 'Seed found, ', ext_key
    else:
        ext_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        print 'Seed generated, ' + ext_key

    ext_name = 'axl' + ext_key
    print 'Name generated, ' + ext_name
    ext_id = 'axl' + ext_key + '@mozilla.org'
    print 'ID generated, ' + ext_id

    if not os.path.exists(path):
        os.makedirs(path)

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

    print 'Success! Web extension at ' + path + ext_name + '.xpi'

    return path + ext_name + '.xpi'

if __name__ == '__main__':
    generate()
