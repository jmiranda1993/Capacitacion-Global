import argparse
import subprocess
import os
import git  # Importa la biblioteca gitpython
import xml.etree.ElementTree as ET
from xml.dom import minidom
import yaml

def create_yaml_file():
    unique_directories = set()
    with open('diff.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'Vlocity/' in line:
                directories = line.split('/')[1:-1]
                unique_directories.add('/'.join(directories))

    git_branch_name = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    fixed_git_branch_name=git_branch_name.replace("/", "-")
    nombrefinal= 'manifest/' + fixed_git_branch_name+'.yaml'
    with open(nombrefinal, 'w') as file:
        file.write("projectPath: ./Vlocity\n")
        file.write("maxDepth: -1\n")
        file.write("autoRetryErrors: true\n")
        file.write("compileOnBuild: false\n")
        file.write("continueAfterError: true\n")
        file.write("autoUpdateSettings: true\n\n")

        file.write("manifest:\n")
        for directory in sorted(list(unique_directories)):
            file.write("- " + directory + "\n")

        file.write("\nOverrideSettings:\n")
        file.write("  DataPacks:\n")
        file.write("    Catalog:\n")
        file.write("      Product2:\n")
        file.write("        MaxDeploy: 1\n")


def eliminar_archivo(ruta_archivo):
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)
        print("El archivo " + ruta_archivo + " ha sido eliminado exitosamente.")
    else:
        print("El archivo a borrar " + ruta_archivo + " no existe.")

def generate_xml(results):
    # Crear elemento raíz del XML
    package = ET.Element('Package')
    package.set('xmlns', 'http://soap.sforce.com/2006/04/metadata')
    
    # Crear diccionario para agrupar los elementos por <name>
    type_dict = {}
    for item in results:
        type_name, member = item
        if type_name not in type_dict:
            type_dict[type_name] = []
        type_dict[type_name].append(member)
    
    # Crear elementos para cada tipo de componente
    for type_name, members in type_dict.items():
        type_element = ET.SubElement(package, 'types')
        for member in members:
            ET.SubElement(type_element, 'members').text = member
        ET.SubElement(type_element, 'name').text = type_name
    
    # Añadir la versión al XML
    version = ET.SubElement(package, 'version')
    version.text = '63.0'
    
    # Crear el objeto ElementTree y escribir el archivo XML con indentación
    tree = ET.ElementTree(package)
    git_branch_name = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    fixed_git_branch_name=git_branch_name.replace("/", "-")
    nombrefinal= 'manifest/' + fixed_git_branch_name+'.xml'
    tree.write(nombrefinal, encoding='UTF-8', xml_declaration=True, short_empty_elements=False)
    
    # Leer el archivo XML y formatearlo con indentación
    with open(nombrefinal, 'r') as file:
        xml_content = file.read()
    formatted_xml = minidom.parseString(xml_content).toprettyxml(indent="    ")
    
    # Guardar el archivo XML formateado
    with open(nombrefinal, 'w') as file:
        file.write(formatted_xml)


def leer_diff_txt():
    diff_file = open("diff.txt", "r")
    diff_lines = diff_file.readlines()
    diff_file.close()

    # Crea una lista vacía para almacenar los resultados
    results = []

    # Itera sobre las líneas del archivo diff
    for line in diff_lines:
        # Si la línea contiene "force-app/main/default"
        if "force-app/main/default" in line:
            # Obtiene el nombre de la carpeta del componente
            foldercomponent = line.split("/")[3]

            if foldercomponent == "apexEmailNotifications":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ApexEmailNotifications"   #Chequeado

            if foldercomponent == "applications":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CustomApplication"     #Chequeado

            if foldercomponent == "approvalProcesses":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ApprovalProcess"     #Chequeado

            if foldercomponent == "assignmentRules":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "AssignmentRules"    #Chequeado

            if foldercomponent == "audience":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Audience"

            if foldercomponent == "aura":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "AuraDefinitionBundle"

            if foldercomponent == "autoResponseRules":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "AutoResponseRules"
            
            if foldercomponent == "brandingSets":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "BrandingSet"

            if foldercomponent == "campaignInfluenceModels":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CampaignInfluenceModel"

            if foldercomponent == "Canvases":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CanvasMetadata"
        

            # Si el nombre de la carpeta es "classes"
            if foldercomponent == "classes":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ApexClass"

            if foldercomponent == "communities":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Community"

            if foldercomponent == "components":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ApexComponent"

            if foldercomponent == "connectedApps":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ConnectedApp"

            if foldercomponent == "contentassets":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ContentAsset"

            if foldercomponent == "corsWhitelistOrigins":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CorsWhitelistOrigin"

            if foldercomponent == "cspTrustedSites":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CspTrustedSite"

            if foldercomponent == "customMetadata":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CustomMetadata"

            if foldercomponent == "customPermissions":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CustomPermission"

            if foldercomponent == "dashboards":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Dashboard"

            if foldercomponent == "documents":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Document"

            if foldercomponent == "duplicateRules":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]+"."+filename.split(".")[1]
                foldercomponent = "DuplicateRule"

            if foldercomponent == "email":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
                item = filename.split(".")[0]
                foldercomponent = "EmailTemplate"
                results.append((foldercomponent,item))
                if line.split("/")[5] != '':
                    obj1 = line.split("/")[4]
                    obj2 = line.split("/")[5]
                    obj2a = obj2.split('.')[0]
                    item = obj1+'/'+obj2a
                    foldercomponent = "EmailTemplate"

            if foldercomponent == "emailservices":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "EmailServicesFunction"

            if foldercomponent == "entitlementProcesses":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "EntitlementProcess"

            if foldercomponent == "escalationRules":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "EscalationRules"

            if foldercomponent == "experiences":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ExperienceBundle"

            if foldercomponent == "flexipages":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "FlexiPage"

            if foldercomponent == "flows":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Flow"

            if foldercomponent == "forecastingTypes":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ForecastingType"

            if foldercomponent == "globalValueSets":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "GlobalValueSet"

            if foldercomponent == "groups":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Group"

            if foldercomponent == "homePageLayouts":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "HomePageLayout"

            if foldercomponent == "iframeWhiteListUrlSettings":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "IframeWhiteListUrlSettings"

            if foldercomponent == "labels":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CustomLabels"

            if foldercomponent == "layouts":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Layout"

            if foldercomponent == "letterhead":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Letterhead"

            if foldercomponent == "lightningExperienceThemes":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "LightningExperienceTheme"
            
            if foldercomponent == "lwc":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "LightningComponentBundle"

            if foldercomponent == "Canvases":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CanvasMetadata"

            if foldercomponent == "managedContentTypes":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ManagedContentType"

            if foldercomponent == "managedTopics":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ManagedTopics"

            if foldercomponent == "matchingRules":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "MatchingRules"

            if foldercomponent == "milestoneTypes":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "MilestoneType"

            if foldercomponent == "moderation":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "KeywordList"
                
            if foldercomponent == "namedCredentials":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "NamedCredential"

            if foldercomponent == "navigationMenus":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "NavigationMenu"

            if foldercomponent == "networkBranding":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "NetworkBranding"

            if foldercomponent == "networks":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Network"

            if foldercomponent == "notificationTypeConfig":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "NotificationTypeConfig"

            if foldercomponent == "notificationtypes":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CustomNotificationType"

            if foldercomponent == "objects":
                obj1=line.split("/")[4]
                obj2=line.split("/")[5]
                # Obtiene el nombre del archivo
                filename = line.split("/")[5]
                # Elimina la extensión del archivo
                item = filename.split(".")[0]

                if obj1 != item:
                    if obj2 == 'fields':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'CustomField'
                    if obj2 == 'index':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'Index'
                    if obj2 == 'businessProcess':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'BusinessProcess'
                    if obj2 == 'recordTypes':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'RecordType'
                    if obj2 == 'compactLayouts':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'CompactLayout'
                    if obj2 == 'webLinks':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'WebLink'
                    if obj2 == 'validationRules':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'ValidationRule'
                    if obj2 == 'sharingReasons':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'SharingReason'
                    if obj2 == 'listViews':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'ListView'
                    if obj2 == 'fieldSets':
                        obj3=line.split("/")[6]
                        item = obj1+'.'+obj3.split('.')[0]
                        foldercomponent = 'FieldSet'
                else:
                    foldercomponent = "CustomObject"

            if foldercomponent == "objectTranslations":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CustomObjectTranslation"

            if foldercomponent == "pages":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ApexPage"

            if foldercomponent == "pathAssistants":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "PathAssistant"

            if foldercomponent == "permissionsetgroups":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "PermissionSetGroup"

            if foldercomponent == "permissionsets":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "PermissionSet"

            if foldercomponent == "mutingpermissionsets":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "MutingPermissionSet"


            if foldercomponent == "presenceUserConfigs":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "PresenceUserConfig"

            if foldercomponent == "profiles":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Profile"

            if foldercomponent == "queueRoutingConfigs":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "QueueRoutingConfig"

            if foldercomponent == "queues":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Queue"
 
            if foldercomponent == "quickActions":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "QuickAction"

            if foldercomponent == "remoteSiteSettings":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "RemoteSiteSetting"

            if foldercomponent == "reports":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Report"

            if foldercomponent == "reportTypes":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ReportType"

            if foldercomponent == "roles":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Role"

            if foldercomponent == "serviceChannels":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ServiceChannel"

            if foldercomponent == "servicePresenceStatuses":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ServicePresenceStatus"

            if foldercomponent == "settings":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Settings"

            if foldercomponent == "sharingRules":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "SharingRules"

            if foldercomponent == "sharingSets":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "SharingSet"

            if foldercomponent == "sites":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CustomSite"

            if foldercomponent == "standardValueSets":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "StandardValueSet"

            if foldercomponent == "standardValueSetTranslations":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "StandardValueSetTranslation"

            if foldercomponent == "staticresources":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "StaticResource"

            if foldercomponent == "tabs":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "CustomTab"

            if foldercomponent == "topicsForObjects":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "TopicsForObjects"

            if foldercomponent == "translations":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Translations"

            if foldercomponent == "triggers":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "ApexTrigger"

            if foldercomponent == "userCriteria":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "UserCriteria"

            if foldercomponent == "workflows":
                # Obtiene el nombre del archivo
                filename = line.split("/")[4]
            
                # Elimina la extensión del archivo
                item = filename.split(".")[0]
                foldercomponent = "Workflow"
            
            # Agrega los resultados a la lista
            if foldercomponent != 'objects':
                results.append((foldercomponent,item))

    results_unique = []
    for result in results:
        if result not in results_unique:
            results_unique.append(result)

    return results_unique


def is_git_repository():
    try:
        repo = git.Repo(search_parent_directories=True)
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

def run_git_diff(rama_origen, rama_destino):
    if not is_git_repository():
        print("No se puede ejecutar, No estás dentro de un repositorio Git.")
        return

    gitcheckout_origen = f"git checkout {rama_origen}"
    gitpull = "git pull"
    gitcheckout_destino = f"git checkout {rama_destino}"
    gitpullorigin_destino = f"git pull origin {rama_destino}"

    subprocess.run(gitcheckout_origen, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # subprocess.run(gitpull, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(gitcheckout_destino, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(gitpull, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(gitcheckout_origen, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(gitpullorigin_destino, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    diff_result = f"git diff --name-only --diff-filter=AMR {rama_destino} {rama_origen} > diff.txt"
    subprocess.run(diff_result, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    parser = argparse.ArgumentParser(description="Captura valores Branch_Origen y Branch_Destino")
    parser.add_argument("Branch_Origen", nargs='?', help="Valor para Branch_Origen")
    parser.add_argument("Branch_Destino", nargs='?', help="Valor para Branch_Destino")

    args = parser.parse_args()

    # Accede a los valores proporcionados
    branch_origen = args.Branch_Origen
    branch_destino = args.Branch_Destino

    if branch_origen is None or branch_destino is None:
        user_input = input("Ingresa el Branch Origen y el Branch Destino. ¿Quieres salir? (Presiona Enter para salir, o ingresa los valores): ")
        if user_input == "":
            return

    if not is_git_repository():
        print("No se puede ejecutar run_git_diff porque no estás dentro de un repositorio Git.")
        return

    print(f"Procesando Delta...")
    print(f"Branch Origen: {branch_origen}")
    print(f"Branch Destino: {branch_destino}")
    print(f"Ubicando las diferencias...")

    # Llama a la función run_git_diff con los valores capturados
    run_git_diff(branch_origen, branch_destino)
    
    # Llama a la función leer_diff_txt y guarda los resultados
    results = leer_diff_txt()


    # Imprime todos los resultados al final
    print("Resultados finales:")
    #for result in results:
    #    print(result)
    
    generate_xml(results)
    print('Creado Archivo XML')
    # create_yaml_file()
    # print('Creado Archivo YAML')

    ruta_archivo_diff = "diff.txt"
    eliminar_archivo(ruta_archivo_diff)

if __name__ == "__main__":
    main()