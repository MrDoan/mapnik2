#ifndef FILE_DATASOURCE_HPP
#define FILE_DATASOURCE_HPP

// mapnik
#include <mapnik/datasource.hpp>

class hello_datasource : public mapnik::datasource 
{
   public:
      // constructor
      // arguments must not change
      hello_datasource(mapnik::parameters const& params, bool bind=true);
      
      // destructor
      virtual ~hello_datasource ();
      
      // mandatory: type of the plugin, used to match at runtime
      int type() const;

      // mandatory: name of the plugin
      static std::string name();

      // mandatory: function to query features by box2d
      // this is called when rendering, specifically in feature_style_processor.hpp
      mapnik::featureset_ptr features(mapnik::query const& q) const;

      // mandatory: function to query features by point (coord2d)
      // not used by rendering, but available to calling applications
      mapnik::featureset_ptr features_at_point(mapnik::coord2d const& pt) const;

      // mandatory: return the box2d of the datasource
      // called during rendering to determine if the layer should be processed
      mapnik::box2d<double> envelope() const;
      
      // mandatory: return the layer descriptor
      mapnik::layer_descriptor get_descriptor() const;
      
      // mandatory: whether to bind the datasource or delay
      void bind() const;

   private:
      // recommended naming convention of datasource members:
      // name_, type_, extent_, and desc_
      static const std::string name_;
      int type_;
      mutable mapnik::layer_descriptor desc_;
      mutable mapnik::box2d<double> extent_;
};


#endif // FILE_DATASOURCE_HPP
