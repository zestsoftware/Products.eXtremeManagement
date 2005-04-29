from Products.Archetypes.public import *
from Products.eXtremeManagement.relations import CustomerProjectRelation

# show description as attribute instead of Metadata, just like CMF
DescriptionSchema = BaseFolderSchema.copy()
DescriptionSchema['description'].isMetadata = False
DescriptionSchema['description'].schemata = 'default'


CustomerSchema = Schema((

    TextField('name',
               index='FieldIndex',
               required=1,
               widget=StringWidget(description="Enter full name, eg. John Smith.",
                                   description_msgid="desc_name",
                                   label="Full Name",
                                   label_msgid="label_name",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    TextField('address',
               index='FieldIndex',
               required=1,
               widget=StringWidget(description="Enter address.",
                                   description_msgid="desc_address",
                                   label="Address",
                                   label_msgid="label_address",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    TextField('zipCode',
               index='FieldIndex',
               required=1,
               widget=StringWidget(description="Enter zip code.",
                                   description_msgid="desc_zipCode",
                                   label="Zip code",
                                   label_msgid="label_zipCode",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    TextField('city',
               index='FieldIndex',
               required=1,
               widget=StringWidget(description="Enter city name.",
                                   description_msgid="desc_city",
                                   label="City",
                                   label_msgid="label_city",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    TextField('country',
               index='FieldIndex',
               required=1,
               widget=StringWidget(description="Enter country.",
                                   description_msgid="desc_country",
                                   label="Country",
                                   label_msgid="label_country",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    IntegerField('phone',
                  index='FieldIndex',
                  required=1,
                  widget=IntegerWidget(description="Enter your phone number.",
                                       description_msgid="desc_phone",
                                       label="Phone",
                                       label_msgid="label_phone",
                                       i18n_domain="eXtremeManagement",
                                       size=30),
                ),
    IntegerField('fax',
                  index='FieldIndex',
                  required=0,
                  widget=IntegerWidget(description="Enter your fax number.",
                                       description_msgid="desc_fax",
                                       label="Fax",
                                       label_msgid="label_fax",
                                       i18n_domain="eXtremeManagement",
                                       size=30),
                ),
    TextField('email',
               index='FieldIndex',
               required=0,
               widget=StringWidget(description="Enter your email address.",
                                   description_msgid="desc_email",
                                   label="E-mail",
                                   label_msgid="label_email",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    TextField('website',
               index='FieldIndex',
               required=0,
               widget=StringWidget(description="Enter your website address.",
                                   description_msgid="desc_website",
                                   label="Website",
                                   label_msgid="label_website",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    TextField('comments',
               required=0,
               widget=TextAreaWidget(description="Enter some comments.",
                                     description_msgid="desc_comments",
                                     label="Comments",
                                     label_msgid="label_comments",
                                     i18n_domain="eXtremeManagement",
                                     rows=3),
             ),

))


ProjectMemberSchema = Schema((

    TextField('fullname',
               index='FieldIndex',
               required=1,
               widget=StringWidget(description="Enter a name, eg. John Smith.",
                                   description_msgid="desc_fullname",
                                   label="Name",
                                   label_msgid="label_fullname",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    IntegerField('phone',
                  index='FieldIndex',
                  required=1,
                  widget=IntegerWidget(description="Enter your phone number.",
                                       description_msgid="desc_phone",
                                       label="Phone",
                                       label_msgid="label_phone",
                                       i18n_domain="eXtremeManagement",
                                       size=30),
                ),
    TextField('email',
               index='FieldIndex',
               required=0,
               widget=StringWidget(description="Enter an email address",
                                   description_msgid="desc_email",
                                   label="E-mail",
                                   label_msgid="label_email",
                                   i18n_domain="eXtremeManagement",
                                   size=30),
             ),
    TextField('comments',
               required=0,
               widget=TextAreaWidget(description="Enter some comments.",
                                     description_msgid="desc_comments",
                                     label="Comments",
                                     label_msgid="label_comments",
                                     i18n_domain="eXtremeManagement",
                                     rows=3),
             ),

))

TaskSchema = Schema((

    TextField('task',
               index='FieldIndex',
               required=1,
               widget=TextAreaWidget(description="Enter task description.",
                                     description_msgid="desc_task",
                                     label="Task",
                                     label_msgid="label_task",
                                     i18n_domain="eXtremeManagement",
                                     rows=3),
             ),
    IntegerField('estimate',
                  index='FieldIndex',
                  required=1,
                  widget=IntegerWidget(description="Enter the estimated time (in hours).",
                                       description_msgid="desc_estimate",
                                       label="Estimate",
                                       label_msgid="label_estimate",
                                       i18n_domain="eXtremeManagement",
                                       size=15),
                ),
    IntegerField('actual',
                  index='FieldIndex',
                  required=0,
                  widget=IntegerWidget(description="Enter the actual time (in hours).",
                                       description_msgid="desc_actual",
                                       label="Actual",
                                       label_msgid="label_actual",
                                       i18n_domain="eXtremeManagement",
                                       size=15),
                ),
    LinesField('assignees',
                index='FieldIndex', 
                required=0,
                vocabulary='_get_assignees',
                widget=MultiSelectionWidget(description="Select the member(s) to assign this task to.",
                                            description_msgid="desc_assignees", 
                                            label="Select Assignees",
                                            label_msgid="label_assignees",
                                            i18n_domain="eXtremeManagement"),
          
              ),

))

ProjectSchema = Schema((

    ReferenceField('customer_project_refenrence',
                    relationship=CustomerProjectRelation.relationship,
                    referenceClass=CustomerProjectRelation,
                    multiValued=1,
                    allowed_types=('Customer',),
                    widget=ReferenceWidget(label="Customers",
                                           label_msgid="label_customers",
                                           description="Reference to a customer.",
                                           description_msgid="description_customer",),
                  ),
#    StringField('project_members',
#                 index='FieldIndex',
#                 required=0,
#                 vocabulary='_get_project_members',
#                 widget=MultiSelectionWidget(description="Select the member(s) for this project.",
#                                             description_msgid="desc_project_memeber",
#                                             label="Select project members",
#                                             label_msgid="label_project_members",
#                                             i18n_domain="eXtremeManagement"),
#
#               ),
))

StorySchema = Schema((

    TextField('mainText',
               required=1,
               widget=RichWidget(description="Enter the main description for this object.",
                                 description_msgid="desc_mainText",
                                 label="Body text",
                                 label_msgid="label_mainText",
                                 i18n_domain="eXtremeManagement",
                                 rows=5),
             ),

))

IterationSchema = Schema((

    LinesField('story_iteration',
               required=0,
               vocabulary='_get_stories',
               widget=InAndOutWidget(label="Stories",
                                     label_msgid="label_stories",
                                     description="Select the stories for this iteration.",
                                     description_msgid="description_stories",
                                     i18n_domain="eXtremeManagement",),
                  ),
))



